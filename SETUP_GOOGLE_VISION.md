# 🤖 Configurar Google Cloud Vision API

## Passos para ativar IA automática no E-Lixo

### 1️⃣ Criar Projeto no Google Cloud

1. Acesse: https://console.cloud.google.com/
2. Clique no seletor de projeto (canto superior esquerdo)
3. Clique em **"NEW PROJECT"**
4. Nome: `E-Lixo`
5. Clique em **"CREATE"**
6. Espere alguns segundos e selecione o novo projeto

---

### 2️⃣ Ativar Vision API

1. No menu superior, procure pela **barra de pesquisa**
2. Digite: `Cloud Vision API`
3. Selecione o resultado
4. Clique em **"ENABLE"**
5. Aguarde a ativação (leva alguns segundos)

---

### 3️⃣ Criar Service Account & Chave JSON

1. No menu esquerdo, vá para: **APIs & Services** → **Credentials**
2. Clique em **"Create Credentials"** → **"Service Account"**
3. Preencha:
   - **Service account name**: `elixo-vision`
   - **Service account ID**: Preenchido automaticamente
   - Clique em **"Create and Continue"**
4. Na tela de permissões:
   - Role: `Basic` → `Editor`
   - Clique em **"Continue"**
5. Clique em **"Done"**

---

### 4️⃣ Gerar e Baixar Chave JSON

1. Na página de Credentials, encontre a service account `elixo-vision`
2. Clique em: **Keys** → **Add Key** → **Create new key**
3. Selecione **JSON**
4. Clique em **"Create"**
5. O arquivo `[seu-projeto-id]-[random].json` será baixado automaticamente

---

### 5️⃣ Configurar no E-Lixo (Local)

1. **Copie o arquivo JSON baixado** para a pasta do projeto:
   ```
   C:\Users\Dev2\Desktop\E-Lixo\
   ```

2. **Defina a variável de ambiente** (no PowerShell, na pasta do projeto):
   ```powershell
   $env:GOOGLE_APPLICATION_CREDENTIALS="C:\Users\Dev2\Desktop\E-Lixo\[seu-arquivo].json"
   ```

3. **Reinicie o Flask** para que a variável tome efeito:
   ```powershell
   .venv-1\Scripts\python app.py
   ```

---

### 6️⃣ Configurar para Produção (Render)

1. Acesse seu dashboard no Render
2. Selecione o serviço E-Lixo
3. Vá para **Environment** (Variáveis de Ambiente)
4. **Conteúdo do arquivo JSON** da chave de serviço, adicione uma variável:
   - **Key**: `GOOGLE_APPLICATION_CREDENTIALS`
   - **Value**: `/etc/secrets/google-cloud-key.json` (ou similar)

5. Adicione também uma variável com o conteúdo do JSON:
   - **Key**: `GOOGLE_CLOUD_KEY_JSON`
   - **Value**: Cole todo o conteúdo do arquivo `.json` entre aspas

6. No `app.py`, o código automaticamente usará a chave se a variável estiver definida.

---

### ✅ Testar a Integração

1. Inicie o servidor Flask:
   ```powershell
   .venv-1\Scripts\python app.py
   ```

2. Abra http://localhost:8000/

3. Faça upload de uma imagem de eletrônico

4. Se funcionou, você verá:
   - ✨ **IA Automática**: Sugestão de categoria detectada pela Google Vision
   - Objetos detectados listados
   - Confiança da classificação

---

## 🎯 O que a IA fará:

- ✅ Detectar objetos na imagem automaticamente
- ✅ Classificar em categorias de lixo eletrônico
- ✅ Mostrar confiança da detecção
- ✅ Sugerir categoria (você pode aceitar ou mudar)
- ✅ Regressar para pHash se a API falhar

---

## 💰 Custos

- Google Cloud Vision: **Primeiras 1.000 requisições/mês GRATIS**
- Depois: ~$1,50 por 1.000 requisições
- Para E-Lixo, é praticamente **gratuito** (a menos que receba muitos uploads)

---

## 🚀 Próximas Etapas

1. Configure a chave JSON
2. Teste localmente
3. Deploy no Render com a variável de ambiente
4. Imagens serão automaticamente reconhecidas! 🎉

---

**Dúvidas?** Verifique os logs do Flask para erros de autenticação.
