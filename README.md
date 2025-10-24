# Gerador de Documentos DOCX

Aplicação Flask para gerar documentos DOCX personalizados a partir de templates, preenchendo automaticamente campos com dados fornecidos pelo usuário.

## 🚀 Funcionalidades

- Interface web simples e intuitiva
- Preenchimento automático de templates DOCX
- Formatação automática de CPF e telefone
- Geração de endereço completo
- Processamento de data no formato português brasileiro

## 📋 Pré-requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

## 🔧 Instalação

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd template_docx
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

3. Instale as dependências:
```bash
pip install flask python-docx docxtpl
```

## 💻 Como usar

1. Inicie o servidor Flask:
```bash
python app.py
```

2. Acesse no navegador:
```
http://localhost:5000
```

3. Preencha o formulário com os dados necessários

4. Clique em "Gerar Documento" para fazer o download do arquivo DOCX gerado

## 📁 Estrutura do Projeto

```
template_docx/
├── app.py              # Aplicação principal Flask
├── modelo.docx         # Template do documento
├── templates/
│   └── index.html      # Interface web
├── .gitignore
└── README.md
```

## 🛠️ Tecnologias Utilizadas

- **Flask** - Framework web
- **python-docx** - Manipulação de arquivos DOCX
- **docxtpl** - Template engine para documentos Word

## 📝 Licença

Este projeto é de uso interno.
