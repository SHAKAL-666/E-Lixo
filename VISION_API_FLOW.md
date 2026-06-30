# 🤖 Fluxo de Classificação Automática com Google Cloud Vision

## Como funciona o upload com IA:

```
┌─────────────────────────────────────────────────────────────────┐
│  1. Você envia uma foto de um eletrônico                         │
└─────────────────┬───────────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────────────────────────────┐
│  2. Sistema valida se é arquivo válido (JPG, PNG, etc)          │
│     ✓ Salva arquivo com nome único                              │
│     ✓ Calcula hash perceptual (pHash) da imagem                 │
└─────────────────┬───────────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────────────────────────────┐
│  3. Verifica duplicatas no catálogo                             │
│     ✓ Se encontrar imagem parecida → mostra match               │
│     ✗ Se não encontrar → continua para IA                       │
└─────────────────┬───────────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────────────────────────────┐
│  4. ⭐ GOOGLE CLOUD VISION API (se credentials OK)              │
│     • Envia imagem para análise remota                          │
│     • Google detecta objetos (ex: "laptop", "keyboard", etc)    │
│     • API retorna labels com confiança                          │
│     • Sistema mapeia para categorias E-Lixo                     │
└─────────────────┬───────────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────────────────────────────┐
│  5. Se Vision API falhar (sem credenciais ou erro):             │
│     Fallback para TensorFlow MobileNetV2 (local, se instalado)  │
└─────────────────┬───────────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────────────────────────────┐
│  6. Retorna SUGESTÕES AUTOMÁTICAS:                              │
│     ✓ Categoria detectada: "Equipamentos de informática"        │
│     ✓ Confiança: 95.3%                                          │
│     ✓ Objetos encontrados: "laptop", "keyboard", "monitor"     │
│     ✓ Você pode ACEITAR ou MODIFICAR                            │
└─────────────────┬───────────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────────────────────────────┐
│  7. Cadastra item no catálogo com:                              │
│     ✓ Imagem salva                                              │
│     ✓ Categoria (confirmada ou editada)                         │
│     ✓ Explicação automática + sua anotação                      │
│     ✓ Hash perceptual para futuras detecções                    │
└─────────────────┬───────────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────────────────────────────┐
│  8. Resultado final:                                            │
│     📸 Imagem catalogada                                         │
│     🏷️  Categoria automática                                    │
│     ✨ Pronta para busca futura                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Exemplo Prático de Resposta da IA:

### Você envia: Foto de um laptop

```json
{
  "matched": false,
  "filename": "laptop_123.jpg",
  "phash": "a1b2c3d4e5f6...",
  
  "suggested": {
    "category": "Equipamentos de informática",
    "confidence": 0.95,
    "neighbors": [...]
  },
  
  "ml_suggestion": {
    "label": "laptop",
    "confidence": 0.987,
    "category": "Equipamentos de informática",
    "explanation": "Computadores, notebooks, monitores, impressoras...",
    "detected_objects": ["laptop", "keyboard", "trackpad", "screen"]
  }
}
```

### Você vê na tela:
```
✨ IA Automática: Equipamentos de informática (confiança 98.7%)
   Objetos detectados: laptop, keyboard, trackpad, screen
   
   [Aceitar Sugestão] [Mudar Categoria]
```

---

## Benefícios:

| Ação | Antes | Depois |
|------|-------|--------|
| **Categorizar imagem** | Manual | Automático ⚡ |
| **Tempo por item** | 30-60s | 5-10s |
| **Erro humano** | Alto | Quase zero |
| **Escala** | Limitada | Sem limite |
| **Qualidade** | Variável | Consistente |

---

## Configuração Rápida:

1. **Gerar chave JSON no Google Cloud** (ver SETUP_GOOGLE_VISION.md)
2. **Definir variável de ambiente**:
   ```powershell
   $env:GOOGLE_APPLICATION_CREDENTIALS="seu-arquivo.json"
   ```
3. **Reiniciar Flask** e pronto! 🚀

---

## Suporte Offline:

Sem credenciais do Google Cloud?
- ✅ Sistema continua funcionando com pHash (detecção de duplicatas)
- ✅ Você pode categorizar manualmente
- ✅ Configure Google Cloud depois quando quiser IA automática

---

## Próximo Passo:

👉 **Deploy no Render com IA ativa**
   - Credenciais seguras no Render
   - Imagens reconhecidas automaticamente online
   - Sem limite de usuários
