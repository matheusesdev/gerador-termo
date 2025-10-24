import io
import locale # <-- 1. Importe o módulo locale
from flask import Flask, render_template, request, send_file
from docxtpl import DocxTemplate
from datetime import datetime

# --- Tenta configurar o locale para Português do Brasil ---
# Isso é necessário para que o mês saia em português (ex: "Abril" em vez de "April")
try:
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_TIME, 'Portuguese_Brazil')
    except locale.Error:
        print("Locale pt_BR não encontrado, usando o padrão do sistema.")


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

# --- APLICAÇÃO FLASK ---
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gerar-documento', methods=['POST'])
def gerar_documento():
    try:
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

        # Formata a data de assinatura usando o locale PT-BR
        data_str = request.form['data_assinatura']
        data_obj = datetime.strptime(data_str, '%Y-%m-%d')
        context['data_assinatura'] = data_obj.strftime('%d de %B de %Y')
        
        doc.render(context)

        file_stream = io.BytesIO()
        doc.save(file_stream)
        file_stream.seek(0)

        nome_arquivo_saida = f"termo_de_reserva_{context['nome_cliente'].replace(' ', '_')}.docx"
        
        return send_file(
            file_stream,
            as_attachment=True,
            download_name=nome_arquivo_saida,
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )

    except Exception as e:
        return f"<h1>Ocorreu um erro:</h1><p>{e}</p><p>Verifique se todos os campos foram preenchidos corretamente.</p>"

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)