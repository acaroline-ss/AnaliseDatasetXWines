#! /usr/bin/python3
import logging
import os
import sys

# Garante que a pasta atual está no path do Python
sys.path.insert(0, os.path.dirname(__file__))

# Importa o APP do app.py
from app import APP
import db

# Configuração de logging
logging.basicConfig(level=logging.INFO,
                  format='%(asctime)s - %(levelname)s - %(message)s',
                  datefmt='%Y-%m-%d %H:%M:%S')

# Conecta ao banco de dados
try:
    db.connect()
    logging.info("✅ Banco de dados conectado com sucesso!")
except Exception as e:
    logging.error(f"❌ Erro ao conectar ao banco: {e}")
    # Não levanta exceção para o app continuar tentando

# Pega a porta do ambiente (Render define isso automaticamente)
port = int(os.environ.get("PORT", 10000))

# Log das rotas disponíveis (útil para debug)
logging.info(f"🚀 App inicializado com {len(APP.url_map._rules)} rotas")

if __name__ == '__main__':
    # Só executa se rodar diretamente (python server.py)
    # No Render, quem roda é o gunicorn, então isso não executa
    logging.info(f"🌐 Servidor rodando em http://0.0.0.0:{port}")
    APP.run(host='0.0.0.0', port=port, debug=False)
