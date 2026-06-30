Resumo do conserto E-Lixo

O que foi feito:
- Corrigido o endpoint `/upload` em `app.py`.
- Removida a condição que retornava `invalid file type` quando a imagem era válida mas não havia vizinhos sugeridos.
- Ajustado o fluxo para sempre salvar o arquivo, calcular `phash`, verificar similaridade e retornar resultado mesmo sem sugestões.
- Atualizado `tests/run_tests.py` para verificar o nome de arquivo retornado pela API nas páginas de catálogo.
- Validado com o script de testes: upload, catálogo e remoção administrativa.

Resultado:
- Upload de imagem JPEG agora funciona novamente.
- Fluxo de catálogo end-to-end está operando corretamente.
- O bug foi fixado em `app.py` e testado com sucesso.
