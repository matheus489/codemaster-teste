# Guia de Deploy no cPanel - testeinterfaces.codemaster-ia.pt

Este projeto contém **dois aplicativos Reflex** que devem ser hospedados no mesmo subdomínio com rotas diferentes.

## 📁 Estrutura do Projeto

```
testeinterfaces.codemaster-ia.pt/
├── copywriter/          # Aplicativo Gerador de Conteúdo IA
│   ├── copywriter/
│   ├── assets/
│   ├── passenger_wsgi.py
│   ├── .htaccess
│   ├── requirements.txt
│   └── rxconfig.py
├── tendencias/          # Aplicativo Monitor de Tendências
│   ├── tendencias/
│   ├── assets/
│   ├── passenger_wsgi.py
│   ├── .htaccess
│   ├── requirements.txt
│   └── rxconfig.py
├── .htaccess            # Configuração principal
└── index.html           # Página de seleção
```

## 🚀 Passos para Deploy

### 1. Preparação no cPanel

1. **Criar o subdomínio**: 
   - No cPanel, vá em **Subdomínios**
   - Crie o subdomínio: `testeinterfaces.codemaster-ia.pt`
   - Anote o diretório onde foi criado (geralmente: `/home/usuario/public_html/testeinterfaces.codemaster-ia.pt`)

2. **Ativar Python App**:
   - No cPanel, vá em **Python App** ou **Setup Python App**
   - Você precisará criar **duas aplicações Python separadas** (uma para cada projeto)

### 2. Upload dos Arquivos

Faça upload de todos os arquivos do projeto para o diretório do subdomínio via **File Manager** ou **FTP**.

A estrutura final deve ser:
```
/home/usuario/public_html/testeinterfaces.codemaster-ia.pt/
├── copywriter/
├── tendencias/
├── .htaccess
└── index.html
```

### 3. Configurar Aplicação Python - COPYWRITER

1. No **Python App** do cPanel:
   - Clique em **Create Application**
   - **Python Version**: 3.11 (ou mais recente)
   - **Application Root**: `/home/usuario/public_html/testeinterfaces.codemaster-ia.pt/copywriter`
   - **Application URL**: `/copywriter`
   - **Application Startup File**: `passenger_wsgi.py`
   - **Application Entry Point**: `application`

2. Depois de criar, anote o caminho do Python Virtual Environment (geralmente algo como):
   `/home/usuario/virtualenv/public_html/testeinterfaces.codemaster-ia.pt/copywriter/3.11/bin/python`

3. **Instalar dependências**:
   - No terminal SSH ou via Python App interface:
   ```bash
   cd /home/usuario/public_html/testeinterfaces.codemaster-ia.pt/copywriter
   source /home/usuario/virtualenv/public_html/testeinterfaces.codemaster-ia.pt/copywriter/3.11/bin/activate
   pip install -r requirements.txt
   ```

### 4. Configurar Aplicação Python - TENDENCIAS

Repita o processo anterior para o projeto tendencias:

1. No **Python App** do cPanel:
   - Clique em **Create Application**
   - **Python Version**: 3.11 (ou mais recente)
   - **Application Root**: `/home/usuario/public_html/testeinterfaces.codemaster-ia.pt/tendencias`
   - **Application URL**: `/tendencias`
   - **Application Startup File**: `passenger_wsgi.py`
   - **Application Entry Point**: `application`

2. **Instalar dependências**:
   ```bash
   cd /home/usuario/public_html/testeinterfaces.codemaster-ia.pt/tendencias
   source /home/usuario/virtualenv/public_html/testeinterfaces.codemaster-ia.pt/tendencias/3.11/bin/activate
   pip install -r requirements.txt
   ```

### 5. Atualizar Arquivos .htaccess

Após criar as aplicações Python, atualize os arquivos `.htaccess` com os caminhos corretos:

#### copywriter/.htaccess
Substitua `[USERNAME]` pelo seu nome de usuário do cPanel:
```
PassengerEnabled On
PassengerAppRoot /home/[USERNAME]/public_html/testeinterfaces.codemaster-ia.pt/copywriter
PassengerBaseURI /copywriter
PassengerPython /home/[USERNAME]/virtualenv/public_html/testeinterfaces.codemaster-ia.pt/copywriter/3.11/bin/python
```

#### tendencias/.htaccess
```
PassengerEnabled On
PassengerAppRoot /home/[USERNAME]/public_html/testeinterfaces.codemaster-ia.pt/tendencias
PassengerBaseURI /tendencias
PassengerPython /home/[USERNAME]/virtualenv/public_html/testeinterfaces.codemaster-ia.pt/tendencias/3.11/bin/python
```

### 6. Configurar Variáveis de Ambiente

Cada aplicação precisa da chave da API OpenAI:

1. No cPanel, vá em **Python App**
2. Para cada aplicação, adicione a variável de ambiente:
   - **Key**: `OPENAI_API_KEY`
   - **Value**: `sua-chave-api-openai-aqui`

   Ou crie um arquivo `.env` em cada pasta:
   ```
   OPENAI_API_KEY=sua-chave-api-openai-aqui
   ```

### 7. Compilar Aplicações Reflex

Antes de colocar em produção, você precisa compilar as aplicações Reflex:

```bash
# Para copywriter
cd /home/usuario/public_html/testeinterfaces.codemaster-ia.pt/copywriter
source /home/usuario/virtualenv/.../copywriter/3.11/bin/activate
reflex export --frontend-only

# Para tendencias
cd /home/usuario/public_html/testeinterfaces.codemaster-ia.pt/tendencias
source /home/usuario/virtualenv/.../tendencias/3.11/bin/activate
reflex export --frontend-only
```

**Nota**: O comando `reflex export` gera os arquivos estáticos necessários para produção.

### 8. Reiniciar Aplicações

No cPanel Python App, clique em **Restart** para cada aplicação criada.

### 9. Verificar URLs

Acesse:
- `https://testeinterfaces.codemaster-ia.pt/` - Página inicial
- `https://testeinterfaces.codemaster-ia.pt/copywriter/` - Gerador de Conteúdo IA
- `https://testeinterfaces.codemaster-ia.pt/tendencias/` - Monitor de Tendências

## ⚠️ Troubleshooting

### Erro: ModuleNotFoundError
- Certifique-se de que todas as dependências foram instaladas no ambiente virtual correto
- Verifique se está usando o Python correto (o do virtualenv)

### Erro: Application not found
- Verifique os caminhos nos arquivos `.htaccess`
- Certifique-se de que `passenger_wsgi.py` está na raiz de cada aplicação
- Verifique se o nome do entry point está correto (`application`)

### Erro: OPENAI_API_KEY not found
- Configure a variável de ambiente no cPanel Python App
- Ou crie um arquivo `.env` na pasta de cada aplicação

### Aplicação não carrega
- Verifique os logs do Passenger no cPanel
- Certifique-se de que as aplicações foram reiniciadas
- Verifique permissões dos arquivos (755 para diretórios, 644 para arquivos)

## 📝 Notas Importantes

1. **Passenger Python**: Certifique-se de que o Passenger está ativado no seu plano de hospedagem cPanel
2. **Reflex em Produção**: Reflex pode precisar de configurações adicionais. Consulte a documentação oficial do Reflex para deploy em produção
3. **SSL**: Configure SSL/HTTPS no cPanel para que as aplicações funcionem corretamente
4. **Limites**: Verifique os limites de recursos (memória, CPU) do seu plano de hospedagem

## 🔗 Documentação Útil

- [Reflex Documentation](https://reflex.dev/docs)
- [Passenger Python Documentation](https://www.phusionpassenger.com/library/config/apache/reference/)
- [cPanel Python App Guide](https://docs.cpanel.net/knowledge-base/web-services/guide-to-python-applications/)


