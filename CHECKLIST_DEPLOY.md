# ✅ Checklist Final - O que enviar para o servidor

## 📦 Arquivos que DEVEM ser enviados

### 📁 Estrutura da pasta principal (testeinterfaces.codemaster-ia.pt/)
```
testeinterfaces.codemaster-ia.pt/
├── .htaccess              ✅ Criado
├── index.html             ✅ Criado
├── README.md              ✅ Criado
└── .gitignore             ✅ Criado
```

### 📁 Projeto COPYWRITER
```
copywriter/
├── copywriter/            ✅ Código fonte
│   ├── __init__.py
│   └── copywriter.py
├── assets/                ✅ Assets estáticos
│   ├── favicon.ico
│   └── styles.css
├── passenger_wsgi.py      ✅ Entry point Passenger
├── .htaccess              ✅ Configuração Passenger
├── requirements.txt       ✅ Dependências Python
├── rxconfig.py            ✅ Configuração Reflex
└── .env                   ⚠️ CRIAR NO SERVIDOR (não enviar com chave)
```

### 📁 Projeto TENDENCIAS
```
tendencias/
├── tendencias/            ✅ Código fonte
│   ├── __init__.py
│   └── tendencias.py
├── assets/                ✅ Assets estáticos
│   ├── favicon.ico
│   └── styles.css
├── passenger_wsgi.py      ✅ Entry point Passenger
├── .htaccess              ✅ Configuração Passenger
├── requirements.txt       ✅ Dependências Python
├── rxconfig.py            ✅ Configuração Reflex
└── .env                   ⚠️ CRIAR NO SERVIDOR (não enviar com chave)
```

## ⚠️ ATENÇÃO: O que NÃO enviar

- ❌ `__pycache__/` - Pasta de cache Python (será gerada automaticamente)
- ❌ `.states/` - Estados do Reflex (será gerado)
- ❌ `.web/` - Build do Reflex (será gerado)
- ❌ `.env` com chaves reais - Criar diretamente no servidor
- ❌ `*.pyc` - Arquivos compilados Python

## 🔧 Ações necessárias ANTES de enviar

### 1. Atualizar arquivos .htaccess

**IMPORTANTE**: Substituir `[USERNAME]` pelo seu username do cPanel nos arquivos:
- `copywriter/.htaccess`
- `tendencias/.htaccess`

### 2. Criar arquivo .env no servidor

Após fazer upload, criar arquivo `.env` em cada pasta:

**copywriter/.env**
```
OPENAI_API_KEY=sua-chave-openai-aqui
```

**tendencias/.env**
```
OPENAI_API_KEY=sua-chave-openai-aqui
```

⚠️ **NUNCA** faça commit ou envie arquivos `.env` com chaves reais para repositórios públicos!

## 📤 Processo de Upload

### Opção 1: Via cPanel File Manager
1. Acessar File Manager no cPanel
2. Navegar até `public_html/testeinterfaces.codemaster-ia.pt/`
3. Fazer upload de TODOS os arquivos (exceto o que está na lista de não enviar)

### Opção 2: Via FTP/SFTP
1. Conectar ao servidor via cliente FTP (FileZilla, WinSCP, etc.)
2. Navegar até `public_html/testeinterfaces.codemaster-ia.pt/`
3. Fazer upload mantendo a estrutura de pastas

## 🚀 Após o upload - Passos no cPanel

### 1. Criar Aplicações Python
- [ ] Criar aplicação Python para `/copywriter`
- [ ] Criar aplicação Python para `/tendencias`
- [ ] Anotar caminhos dos virtualenvs

### 2. Atualizar .htaccess
- [ ] Atualizar `copywriter/.htaccess` com username correto
- [ ] Atualizar `tendencias/.htaccess` com username correto
- [ ] Atualizar caminhos do Python nos .htaccess

### 3. Instalar Dependências
- [ ] Ativar virtualenv do copywriter
- [ ] Instalar `requirements.txt` do copywriter
- [ ] Ativar virtualenv do tendencias
- [ ] Instalar `requirements.txt` do tendencias

### 4. Configurar Variáveis de Ambiente
- [ ] Criar `.env` em `copywriter/` com OPENAI_API_KEY
- [ ] Criar `.env` em `tendencias/` com OPENAI_API_KEY
- [ ] OU configurar via interface Python App do cPanel

### 5. Compilar Aplicações Reflex
- [ ] Executar `reflex export --frontend-only` no copywriter
- [ ] Executar `reflex export --frontend-only` no tendencias

### 6. Reiniciar Aplicações
- [ ] Reiniciar aplicação copywriter no cPanel
- [ ] Reiniciar aplicação tendencias no cPanel

### 7. Testar
- [ ] Acessar `https://testeinterfaces.codemaster-ia.pt/`
- [ ] Acessar `https://testeinterfaces.codemaster-ia.pt/copywriter/`
- [ ] Acessar `https://testeinterfaces.codemaster-ia.pt/tendencias/`

## 📝 Resumo do que está PRONTO

✅ Todos os arquivos de configuração criados
✅ `passenger_wsgi.py` para ambos os projetos
✅ `.htaccess` para ambos os projetos
✅ `requirements.txt` atualizados
✅ `index.html` página inicial criada
✅ Documentação completa no `DEPLOY_CPANEL.md`

## ⚠️ Lembre-se

1. **Username**: Substituir `[USERNAME]` nos arquivos `.htaccess`
2. **API Key**: Não enviar `.env` com chaves reais - criar no servidor
3. **Compilar**: Reflex precisa ser compilado com `reflex export --frontend-only`
4. **Permissões**: Verificar permissões dos arquivos (755 para pastas, 644 para arquivos)

## 🆘 Se algo não funcionar

Consulte o arquivo `DEPLOY_CPANEL.md` para troubleshooting detalhado e verifique:
- Logs do Passenger no cPanel
- Logs de erro do Python
- Permissões de arquivos
- Caminhos nos arquivos `.htaccess`


