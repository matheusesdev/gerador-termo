# 🚀 Guias de Deploy - Gerador de Termos

Este documento contém instruções para fazer deploy da aplicação em diferentes plataformas.

---

## 📊 Comparação de Plataformas

| Plataforma | Cold Start | Custo Free | Facilidade | Recomendação |
|------------|------------|------------|------------|--------------|
| **Fly.io** | ⚡ Muito rápido | Generoso | Média | ⭐ **Melhor para Flask** |
| **Railway** | ⚡ Rápido | Limitado | Fácil | ⭐ Boa alternativa |
| **Vercel** | 🐌 Pode ser lento | Generoso | Fácil | ❌ Melhor para Next.js |
| **Render** | 🐌 Lento (atual) | Sim | Fácil | ⚠️ Problema atual |

---

## 1️⃣ Deploy no Fly.io (RECOMENDADO)

### Por que Fly.io?
- ⚡ **Sem cold start perceptível** - instâncias iniciam em ~1 segundo
- 🌎 Servidores no Brasil (região GRU - São Paulo)
- 💰 Free tier generoso: 3 VMs compartilhadas, 160GB bandwidth
- 🐳 Suporte nativo a Docker

### Passo a passo:

#### 1. Instalar o Fly CLI
```powershell
# Baixe e instale do site oficial
irm https://fly.io/install.ps1 | iex
```

#### 2. Fazer login
```powershell
fly auth login
```

#### 3. Criar a aplicação
```powershell
# No diretório do projeto
cd "C:\Users\matheusespiritosanto\OneDrive - VCA Construtora\Área de Trabalho\template_docx"

# Criar app (nome: gerador-termo)
fly apps create gerador-termo
```

#### 4. Deploy
```powershell
# Fazer o deploy
fly deploy

# Abrir no navegador
fly open
```

#### 5. Configurar domínio (opcional)
```powershell
# Ver domínio atual
fly info

# Adicionar domínio customizado
fly certs add seudominio.com
```

### Comandos úteis:
```powershell
# Ver logs em tempo real
fly logs

# Ver status da aplicação
fly status

# Escalar para mais instâncias
fly scale count 2

# Ver custo atual
fly dashboard
```

---

## 2️⃣ Deploy no Railway

### Por que Railway?
- 🎯 **Muito fácil** - deploy com 3 cliques
- 🔄 Deploy automático do GitHub
- 💰 $5 de crédito grátis por mês
- ⚡ Cold start razoável (~3-5 segundos)

### Passo a passo:

#### 1. Criar conta
- Acesse: https://railway.app
- Faça login com GitHub

#### 2. Deploy direto do GitHub
1. Clique em **"New Project"**
2. Selecione **"Deploy from GitHub repo"**
3. Escolha o repositório `gerador-termo`
4. Railway detecta automaticamente que é Python/Flask
5. Clique em **"Deploy"**

#### 3. Configurar porta (se necessário)
```powershell
# Railway define PORT automaticamente, mas se precisar:
# Vá em Settings > Variables
# Adicione: PORT = 8080
```

#### 4. Gerar domínio
1. Vá na aba **"Settings"**
2. Clique em **"Generate Domain"**
3. Copie o URL gerado

### Vantagens:
- ✅ Zero configuração
- ✅ Deploy automático a cada push no GitHub
- ✅ Banco de dados integrado (se precisar)

---

## 3️⃣ Deploy no Vercel

### ⚠️ Aviso: Vercel é melhor para Next.js/Node.js

O Vercel funciona, mas não é ideal para Flask. Cold starts podem ser lentos.

### Passo a passo:

#### 1. Instalar Vercel CLI
```powershell
npm install -g vercel
```

#### 2. Fazer login
```powershell
vercel login
```

#### 3. Deploy
```powershell
cd "C:\Users\matheusespiritosanto\OneDrive - VCA Construtora\Área de Trabalho\template_docx"
vercel
```

#### 4. Deploy em produção
```powershell
vercel --prod
```

### Limitações no Vercel:
- ❌ Cold starts podem ser lentos (5-10 segundos)
- ❌ Serverless não ideal para Flask
- ❌ Limite de 10 segundos por requisição

---

## 4️⃣ Deploy no Google Cloud Run

### Por que Cloud Run?
- ⚡ Rápido e escalável
- 💰 Free tier: 2 milhões de requisições/mês
- 🌍 Rede global do Google

### Passo a passo:

#### 1. Instalar Google Cloud SDK
```powershell
# Baixe de: https://cloud.google.com/sdk/docs/install
```

#### 2. Login e configurar projeto
```powershell
gcloud auth login
gcloud config set project SEU-PROJETO-ID
```

#### 3. Build e deploy
```powershell
cd "C:\Users\matheusespiritosanto\OneDrive - VCA Construtora\Área de Trabalho\template_docx"

# Build da imagem
gcloud builds submit --tag gcr.io/SEU-PROJETO-ID/gerador-termo

# Deploy no Cloud Run
gcloud run deploy gerador-termo `
  --image gcr.io/SEU-PROJETO-ID/gerador-termo `
  --platform managed `
  --region southamerica-east1 `
  --allow-unauthenticated
```

---

## 🎯 Recomendação Final

### Para seu caso (Flask + problema de cold start):

**1ª Opção: Fly.io** ⭐⭐⭐⭐⭐
- Melhor performance
- Sem cold start perceptível
- Servidores no Brasil

**2ª Opção: Railway** ⭐⭐⭐⭐
- Muito fácil de usar
- Bom custo-benefício
- Deploy automático

**3ª Opção: Google Cloud Run** ⭐⭐⭐
- Escalabilidade infinita
- Mais complexo de configurar

**Evitar: Vercel** ⭐⭐
- Não otimizado para Flask
- Cold starts persistem

---

## 📝 Próximos Passos

1. Escolha a plataforma (recomendo **Fly.io**)
2. Siga o passo a passo acima
3. Teste o desempenho
4. Se quiser, posso configurar deploy automático via GitHub Actions

**Qual plataforma você quer experimentar primeiro?**
