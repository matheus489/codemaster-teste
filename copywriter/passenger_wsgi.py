"""
Passenger WSGI entry point para aplicação Reflex - Copywriter
"""
import sys
import os

# Adiciona o diretório do projeto ao path do Python
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

# Importa a aplicação Reflex
from copywriter.copywriter import app

# Reflex usa FastAPI/Starlette internamente
# O objeto app tem um atributo 'api' que é a aplicação ASGI/WSGI
# Para Passenger, precisamos exportar como 'application'

# Verifica diferentes formas de acessar a aplicação web
if hasattr(app, 'api'):
    # Reflex v0.8+ usa app.api
    application = app.api
elif hasattr(app, 'get_app'):
    # Método alternativo
    application = app.get_app()
elif hasattr(app, '_get_api'):
    # Método interno (não recomendado, mas pode funcionar)
    application = app._get_api()
else:
    # Fallback: tenta usar o app diretamente
    application = app
