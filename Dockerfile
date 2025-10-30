# Use Python 3.11 slim para imagem menor
FROM python:3.11-slim

# Define diretório de trabalho
WORKDIR /app

# Copia arquivos de dependências
COPY requirements.txt .

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código da aplicação
COPY . .

# Cria pasta para arquivos gerados
RUN mkdir -p generated

# Expõe a porta 8080 (padrão para Cloud Run e outros)
EXPOSE 8080

# Comando para iniciar o servidor com Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "app:app"]
