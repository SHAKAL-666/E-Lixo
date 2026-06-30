# Catalogador de Lixo Eletrônico (protótipo)

Protótipo de aplicação web para catalogar imagens de lixo eletrônico e detectar duplicatas. O app grava imagens enviadas e usa pHash para identificar imagens já conhecidas; quando desconhecida, pede que o usuário escolha uma categoria e envie uma explicação.

Funcionalidades:
- Upload de imagens e suporte a captura via câmera em smartphones (input `capture="environment"`).
- Detecção de imagens duplicadas por pHash.
- Armazenamento de imagem em `uploads/` e metadados em banco SQLite (`data/images.db`).

Categorias padrão:
- Equipamentos de informática
- Dispositivos de comunicação
- Equipamentos de áudio e vídeo
- Pilhas e baterias
- Carregadores e cabos
- Eletrodomésticos eletrônicos
- Equipamentos de iluminação
- Componentes eletrônicos

Como rodar (Windows):

1. Criar e ativar um ambiente virtual (opcional mas recomendado):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Instalar dependências:

```powershell
pip install -r requirements.txt
```

3. Rodar o servidor:

```powershell
python app.py
```

4. Abrir no navegador: http://localhost:8000

Para ver os itens cadastrados acesse: http://localhost:8000/catalogs

Notas:
- Este é um protótipo simples que usa comparação por pHash. Conforme o catálogo crescer, a detecção automática ficará mais eficaz.
- Próximos passos possíveis: integrar um modelo de visão computacional para classificação automática, otimizar banco para buscas por similaridade, adicionar autenticação de usuários.

Deployment (recommended)
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
