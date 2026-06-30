# E-Lixo — Catalogador Inteligente de Lixo Eletrônico 🤖

Aplicação web moderna para catalogar e gerenciar imagens de lixo eletrônico com **classificação automática via IA** (Google Cloud Vision API).

## ✨ Funcionalidades

### 📸 Upload & Captura
- ✅ Upload de imagens (JPG, PNG, GIF, BMP)
- ✅ Captura via câmera em smartphones (`capture="environment"`)
- ✅ Preview da imagem antes de catalogar
- ✅ Sugestões automáticas de categoria

### 🤖 Classificação Inteligente (Google Cloud Vision API)
- ✅ Reconhecimento automático de objetos na imagem
- ✅ Mapeamento automático para categorias E-Lixo
- ✅ Confiança da detecção exibida
- ✅ Fallback para TensorFlow se Vision API indisponível
- ✅ Funciona 100% sem IA também (apenas pHash)

### 🔍 Detecção de Duplicatas
- ✅ pHash (perceptual hash) para identificar imagens parecidas
- ✅ Evita entradas repetidas no catálogo
- ✅ Busca rápida por similaridade

### 📊 Catálogo Visual
- ✅ Grade de itens com filtro por categoria
- ✅ Modal de visualização em tamanho maior
- ✅ Descrições automáticas por categoria
- ✅ Armazenamento em SQLite

### 🎨 Interface Moderna
- ✅ **Dark Mode / Light Mode** (toggle na navbar)
- ✅ Design responsivo (mobile, tablet, desktop)
- ✅ Ícones Font Awesome em categorias e features
- ✅ Animações suaves e feedback visual
- ✅ Bootstrap 5.3 com tema customizado

### 🔐 Admin Panel
- ✅ Login seguro com credenciais de admin
- ✅ Visualizar todos os itens catalogados
- ✅ Deletar itens com um clique
- ✅ Sessões persistentes

---

## 🎯 Categorias Suportadas

1. 💻 Equipamentos de informática
2. 📱 Dispositivos de comunicação
3. 📺 Equipamentos de áudio e vídeo
4. 🔋 Pilhas e baterias
5. 🔌 Carregadores e cabos
6. 🏠 Eletrodomésticos eletrônicos
7. 💡 Equipamentos de iluminação
8. 🔧 Componentes eletrônicos

---

## 🚀 Quick Start (Windows)

### 1. Clone e Navegue

```powershell
cd C:\Users\Dev2\Desktop\E-Lixo
```

### 2. Ativar Ambiente Virtual

```powershell
.\.venv-1\Scripts\Activate.ps1
```

### 3. Instalar Dependências

```powershell
pip install -r requirements.txt
```

### 4. Rodar Servidor

```powershell
python app.py
```

### 5. Abrir no Navegador

- 🏠 **Home (Upload)**: http://localhost:8000/
- 📚 **Catálogo**: http://localhost:8000/catalogs
- 🔐 **Admin**: http://localhost:8000/admin
  - Usuário: `admin`
  - Senha: `password`

---

## 🤖 Configurar Google Cloud Vision API (Opcional)

Para ativar classificação automática com IA:

1. Acesse: https://console.cloud.google.com/
2. Crie projeto → Ative Cloud Vision API
3. Crie Service Account e baixe chave JSON
4. Defina variável de ambiente:
   ```powershell
   $env:GOOGLE_APPLICATION_CREDENTIALS="C:\caminho\seu-arquivo.json"
   ```
5. Teste com: `python test_vision_api.py`

📖 **Guia detalhado**: Ver arquivo [`SETUP_GOOGLE_VISION.md`](SETUP_GOOGLE_VISION.md)

---

## 🌐 Deploy Online (Render.com)

Aplicação pronta para deploy em produção:

1. Conecte seu repositório GitHub ao Render
2. Configure variáveis de ambiente (SECRET_KEY, admin creds, Google Cloud Key)
3. Render detecta automaticamente `Procfile` e faz deploy
4. Site fica online com domínio grátis em `https://seu-app.render.com`

📖 **Detalhes**: Ver arquivo [`render.yaml`](render.yaml)

---

## 📁 Estrutura do Projeto

```
E-Lixo/
├── app.py                      # Flask app principal com todas as rotas
├── requirements.txt            # Dependências Python
├── Procfile                    # Configuração para deploy (gunicorn)
├── render.yaml                 # Configuração do Render
├── SETUP_GOOGLE_VISION.md      # Guia de configuração da IA
├── VISION_API_FLOW.md          # Diagrama do fluxo de classificação
├── test_vision_api.py          # Teste da Vision API
├── .env.example                # Variáveis de ambiente (exemplo)
├── .gitignore                  # Arquivos ignorados pelo Git
├── templates/
│   ├── base.html               # Template base (CSS/JS compartilhado)
│   ├── index.html              # Página de upload
│   ├── catalogs.html           # Listagem de itens
│   ├── login.html              # Login de admin
│   └── admin.html              # Painel administrativo
├── uploads/                    # Imagens enviadas (gitignored)
├── data/
│   └── images.db               # Banco SQLite (gitignored)
└── tests/
    ├── run_tests.py            # Testes básicos
    ├── test_health.py          # Teste do health endpoint
    └── test_complete_flow.py   # Suite de testes e2e
```

---

## 📋 Endpoints da API

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/` | Página inicial (upload) |
| POST | `/upload` | Upload de imagem + análise |
| GET | `/catalogs` | Lista todos os itens |
| POST | `/catalog` | Salva item no catálogo |
| GET | `/login` | Página de login |
| POST | `/login` | Autentica admin |
| GET | `/logout` | Encerra sessão |
| GET | `/admin` | Painel administrativo |
| POST | `/admin/delete/<id>` | Remove item |
| GET | `/healthz` | Health check |

---

## 🔧 Configuração via Variáveis de Ambiente

```powershell
# Flask
$env:FLASK_DEBUG=1                    # Modo debug
$env:SECRET_KEY="sua-chave-secreta"  # Chave de sessão

# Admin
$env:E_LIXO_ADMIN_USER="admin"       # Usuário admin
$env:E_LIXO_ADMIN_PASS="password"    # Senha admin

# Servidor
$env:HOST="0.0.0.0"                  # Host
$env:PORT="8000"                     # Porta

# Google Cloud Vision (para IA)
$env:GOOGLE_APPLICATION_CREDENTIALS="path/to/key.json"
```

---

## 📦 Dependências Principais

- **Flask 2.2.5** — Web framework
- **Pillow 12.2.0** — Processamento de imagens
- **imagehash 4.3.1** — Detecção de duplicatas (pHash)
- **google-cloud-vision 3.15.0** — IA de classificação (opcional)
- **gunicorn 20.1.0** — WSGI server (produção)

---

## ✅ Testes

Execute os testes para validar funcionalidades:

```powershell
# Todos os testes
python -m unittest discover -s tests -p "test_*.py"

# Teste específico
python tests/test_health.py

# Teste de Vision API
python test_vision_api.py
```

---

## 🎨 Tema & Customização

- **Cores**: Variáveis CSS customizáveis em `base.html`
- **Dark Mode**: Toggle automático com persistência em localStorage
- **Ícones**: Font Awesome 6.4 integrado
- **Bootstrap**: v5.3.2 com tema dark/light

---

## 🐛 Troubleshooting

### "Arquivo de imagem inválido"
→ Use formatos: JPG, PNG, GIF, BMP

### "Vision API não funciona"
→ Verifique `GOOGLE_APPLICATION_CREDENTIALS` configurada
→ Rode `python test_vision_api.py` para diagnóstico

### "Porta 8000 já em uso"
→ Mude porta: `$env:PORT=8001; python app.py`

---

## 📝 Licença & Contribuições

Protótipo de pesquisa/educação. Contribuições são bem-vindas!

---

## 🎯 Roadmap Futuro

- [ ] Busca por similaridade (PostgreSQL + pgvector)
- [ ] Exportar catálogo em CSV/JSON
- [ ] Multi-tenancy (múltiplos usuários)
- [ ] API pública para integração
- [ ] Dashboard analítico
- [ ] Notificações em tempo real

---

**Perguntas?** Abra uma issue no GitHub! 🚀

## Deployment (recommended)
-----------------------

Recomendo usar um serviço como Render (https://render.com) ou Railway para hospedar a aplicação sem depender do seu computador.

Preparação básica no repositório:

1. Adicionamos um `Procfile` para execução com `gunicorn` e removemos `tensorflow` das dependências por ser muito pesado para builds automáticos. Se quiser ML, instale `tensorflow-cpu` manualmente na imagem ou use um serviço separado.

2. Para deploy no Render (fluxo recomendado):
	- Suba o código para um repositório no GitHub.
	- Na dashboard do Render, crie um novo Web Service e conecte ao repositório GitHub.
	- Em Build Command use: `pip install -r requirements.txt`
	- Em Start Command deixe o `Procfile` cuidar do start (`web: gunicorn app:app --bind 0.0.0.0:$PORT`).
	- Configure variáveis de ambiente: `SECRET_KEY`, `E_LIXO_ADMIN_USER`, `E_LIXO_ADMIN_PASS`.

3. Persistência de uploads:
	- A solução de produção deve usar um bucket S3 (ou equivalente) para armazenar uploads.
	- Atualmente a app grava em `uploads/` local — isso é efêmero em muitas plataformas. Recomendo adaptar o app para usar S3 e configurar via `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` e `S3_BUCKET`.

Comandos úteis para preparar o repositório localmente (PowerShell):
```powershell
cd C:\Users\Dev2\Desktop\E-Lixo
.venv-1\Scripts\git.exe init
.venv-1\Scripts\git.exe add .
.venv-1\Scripts\git.exe commit -m "Initial commit: E-Lixo"
```

Depois crie o repositório no GitHub e faça:
```powershell
.venv-1\Scripts\git.exe remote add origin https://github.com/SEU_USUARIO/SEU_REPO.git
.venv-1\Scripts\git.exe branch -M main
.venv-1\Scripts\git.exe push -u origin main
```

Se quiser, posso automatizar a criação do repo no GitHub e fazer o push (vou precisar de um Personal Access Token com `repo` scope), ou posso gerar um passo a passo curto para você executar. Diga qual prefere.
