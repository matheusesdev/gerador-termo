# 🚀 Guia de Deploy no Render

## Arquivos de Configuração Criados

✅ `Procfile` - Define como iniciar a aplicação
✅ `build.sh` - Script de build para instalação de dependências
✅ `runtime.txt` - Versão do Python
✅ `requirements.txt` - Atualizado com gunicorn
✅ `app.py` - Configurado para produção

## 📋 Passo a Passo para Deploy

### 1. Criar Conta no Render
- Acesse: https://render.com
- Clique em **"Get Started"**
- Faça login com sua conta do GitHub

### 2. Criar Novo Web Service
1. No dashboard do Render, clique em **"New +"**
2. Selecione **"Web Service"**
3. Conecte seu repositório GitHub:
   - Clique em **"Connect account"** (se necessário)
   - Procure por: **gerador-termo**
   - Clique em **"Connect"**

### 3. Configurar o Web Service

Preencha os campos:

- **Name:** `gerador-termo` (ou escolha outro nome)
- **Region:** `Oregon (US West)` (ou o mais próximo)
- **Branch:** `main`
- **Root Directory:** deixe vazio
- **Runtime:** `Python 3`
- **Build Command:** `./build.sh`
- **Start Command:** `gunicorn app:app`

### 4. Plano Gratuito
- Selecione o plano **"Free"**
- ⚠️ O plano gratuito tem limitações:
  - Aplicação "dorme" após 15 minutos de inatividade
  - Primeira requisição após inatividade pode demorar ~1 minuto
  - 750 horas gratuitas por mês

### 5. Deploy
1. Clique em **"Create Web Service"**
2. Aguarde o build e deploy (5-10 minutos)
3. Você verá os logs em tempo real
4. Quando aparecer "Your service is live 🎉", está pronto!

### 6. Acessar sua Aplicação
- A URL será algo como: `https://gerador-termo.onrender.com`
- O Render fornecerá a URL completa no dashboard

## 🔄 Atualizações Futuras

Depois do primeiro deploy, qualquer `git push` para o GitHub acionará automaticamente um novo deploy no Render!

```bash
git add .
git commit -m "Sua mensagem"
git push
```

## ⚡ Dicas Importantes

1. **Primeira Requisição Lenta:** Após inatividade, o app demora ~1 minuto para "acordar"
2. **Logs:** Use a aba "Logs" no Render para ver erros
3. **Upgrade:** Se precisar de melhor performance, considere o plano pago ($7/mês)

## 🆘 Solução de Problemas

Se o deploy falhar:
1. Verifique os logs no Render
2. Certifique-se que todos os arquivos estão no GitHub
3. Verifique se o `build.sh` tem permissão de execução

---

**✅ Seu projeto está pronto para deploy!**
Acesse https://render.com e siga os passos acima.
