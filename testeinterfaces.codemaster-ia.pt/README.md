# testeinterfaces.codemaster-ia.pt

Este é o subdomínio que hospeda duas aplicações Reflex:

1. **Copywriter** - Gerador de Conteúdo IA (`/copywriter/`)
2. **Tendencias** - Monitor de Tendências (`/tendencias/`)

## 📂 Estrutura

```
testeinterfaces.codemaster-ia.pt/
├── copywriter/        # Aplicação 1: Gerador de Conteúdo
├── tendencias/        # Aplicação 2: Monitor de Tendências
├── .htaccess         # Configuração principal do subdomínio
└── index.html        # Página inicial de seleção
```

## 🚀 Instruções de Deploy

Consulte o arquivo `DEPLOY_CPANEL.md` na raiz do projeto para instruções completas de deploy no cPanel.

## ⚙️ Configuração

### Variáveis de Ambiente Necessárias

Cada aplicação precisa da seguinte variável de ambiente:

- `OPENAI_API_KEY`: Chave da API OpenAI

Configure-as no cPanel Python App ou via arquivo `.env` em cada pasta de aplicação.

## 🔗 URLs

- Página inicial: `https://testeinterfaces.codemaster-ia.pt/`
- Copywriter: `https://testeinterfaces.codemaster-ia.pt/copywriter/`
- Tendencias: `https://testeinterfaces.codemaster-ia.pt/tendencias/`


