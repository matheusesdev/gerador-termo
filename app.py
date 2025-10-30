import io
import os
import uuid
from flask import Flask, render_template, request, send_file, jsonify
from docxtpl import DocxTemplate
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from datetime import datetime

# --- DICIONÁRIO DE MESES EM PORTUGUÊS ---
# Solução independente de locale para garantir meses em PT-BR
MESES_PT = {
    1: 'janeiro',
    2: 'fevereiro',
    3: 'março',
    4: 'abril',
    5: 'maio',
    6: 'junho',
    7: 'julho',
    8: 'agosto',
    9: 'setembro',
    10: 'outubro',
    11: 'novembro',
    12: 'dezembro'
}

def formatar_data_ptbr(data_obj):
    """Formata data para formato brasileiro: 'dd de mês de yyyy'"""
    dia = data_obj.day
    mes = MESES_PT[data_obj.month]
    ano = data_obj.year
    return f"{dia} de {mes} de {ano}"


# --- FUNÇÕES AUXILIARES DE FORMATAÇÃO ---
def formatar_cpf(cpf_str):
    cpf_limpo = "".join(filter(str.isdigit, cpf_str))
    if len(cpf_limpo) != 11:
        return cpf_str
    return f"{cpf_limpo[:3]}.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-{cpf_limpo[9:]}"

def formatar_telefone(tel_str):
    tel_limpo = "".join(filter(str.isdigit, tel_str))
    if len(tel_limpo) == 10:
        return f"({tel_limpo[:2]}) {tel_limpo[2:6]}-{tel_limpo[6:]}"
    if len(tel_limpo) == 11:
        return f"({tel_limpo[:2]}) {tel_limpo[2:7]}-{tel_limpo[7:]}"
    return tel_str

def proteger_documento(caminho_arquivo):
    """
    Adiciona proteção ao documento Word para evitar edições.
    O documento fica somente leitura, mas pode ser impresso e copiado.
    """
    try:
        # Abre o documento com python-docx
        doc = Document(caminho_arquivo)
        
        # Acessa as configurações do documento
        settings = doc.settings
        element = settings.element
        
        # Cria elemento de proteção
        doc_protection = OxmlElement('w:documentProtection')
        doc_protection.set(qn('w:edit'), 'readOnly')
        doc_protection.set(qn('w:enforcement'), '1')
        
        # Remove proteção anterior se existir
        for child in list(element):
            if child.tag == qn('w:documentProtection'):
                element.remove(child)
        
        # Adiciona nova proteção
        element.append(doc_protection)
        
        # Salva o documento protegido
        doc.save(caminho_arquivo)
        return True
    except Exception as e:
        print(f"Erro ao proteger documento: {e}")
        return False

# --- APLICAÇÃO FLASK ---
app = Flask(__name__)

# Criar pasta para documentos gerados temporariamente
# No Vercel, usar /tmp para arquivos temporários
GENERATED_FOLDER = '/tmp/generated' if os.environ.get('VERCEL') else 'generated'
if not os.path.exists(GENERATED_FOLDER):
    os.makedirs(GENERATED_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gerar-documento', methods=['POST'])
def gerar_documento():
    try:
        # Seleciona o modelo baseado no empreendimento escolhido
        empreendimento = request.form.get('empreendimento', 'connect')
        if empreendimento == 'dona':
            doc = DocxTemplate("modelodona.docx")
        else:
            doc = DocxTemplate("modelo.docx")
        
        logradouro = request.form['logradouro']
        numero = request.form['numero']
        bairro = request.form['bairro']
        cidade = request.form['cidade']
        estado = request.form['estado'].upper()
        endereco_completo = f"{logradouro}, {numero}, {bairro}, {cidade}/{estado}"
        
        context = {
            'nome_cliente': request.form['nome_cliente'],
            'estado_civil': request.form['estado_civil'],
            'profissao': request.form['profissao'],
            'rg_cliente': request.form['rg_cliente'],
            'rg_orgao': request.form['rg_orgao'],
            'cpf_cliente': formatar_cpf(request.form['cpf_cliente']),
            'telefone_cliente': formatar_telefone(request.form['telefone_cliente']),
            'endereco_cliente': endereco_completo,
            'cep_cliente': request.form['cep_cliente'],
            'email_cliente': request.form['email_cliente'],
            'banco': request.form['banco'],
            'agencia': request.form['agencia'],
            'conta': request.form['conta'],
            'chave_pix': request.form['chave_pix'],
            'nome_corretor': request.form['nome_corretor'],
            'cpf_cnpj_corretor': request.form['cpf_cnpj_corretor'],
        }

        # Formata a data de assinatura usando função personalizada PT-BR
        data_str = request.form['data_assinatura']
        data_obj = datetime.strptime(data_str, '%Y-%m-%d')
        data_formatada = formatar_data_ptbr(data_obj)
        print(f"DEBUG - Data recebida: {data_str}")
        print(f"DEBUG - Data formatada: {data_formatada}")
        context['data_assinatura'] = data_formatada
        
        doc.render(context)

        # Gera nome único para o arquivo
        nome_arquivo_saida = f"termo_de_reserva_{context['nome_cliente'].replace(' ', '_')}_{uuid.uuid4().hex[:8]}.docx"
        caminho_arquivo = os.path.join(GENERATED_FOLDER, nome_arquivo_saida)
        
        # Salva o arquivo no disco
        doc.save(caminho_arquivo)
        
        # Protege o documento contra edições
        proteger_documento(caminho_arquivo)
        
        # Se a requisição for AJAX (via fetch), retorna JSON
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'success': True,
                'download_url': f'/download/{nome_arquivo_saida}',
                'filename': nome_arquivo_saida
            })
        
        # Senão, retorna o arquivo diretamente (comportamento antigo)
        file_stream = io.BytesIO()
        doc.save(file_stream)
        file_stream.seek(0)
        
        return send_file(
            file_stream,
            as_attachment=True,
            download_name=nome_arquivo_saida,
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )

    except Exception as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'success': False,
                'error': str(e)
            }), 400
        return f"<h1>Ocorreu um erro:</h1><p>{e}</p><p>Verifique se todos os campos foram preenchidos corretamente.</p>"

@app.route('/download/<filename>')
def download_file(filename):
    """Rota para download do arquivo gerado"""
    try:
        caminho_arquivo = os.path.join(GENERATED_FOLDER, filename)
        return send_file(
            caminho_arquivo,
            as_attachment=True,
            download_name=filename,
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
    except Exception as e:
        return f"<h1>Erro ao baixar arquivo:</h1><p>{e}</p>", 404

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)