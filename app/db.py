import logging
import sqlite3
import re
import os

global DB, DB_FILE

# CAMINHO CORRETO PARA O RENDER:
# O banco de dados deve estar na MESMA PASTA que este arquivo
DB_FILE = os.path.join(os.path.dirname(__file__), 'wines.db')

DB = dict()

def connect():
    global DB, DB_FILE
    try:
        c = sqlite3.connect(DB_FILE, check_same_thread=False)
        c.row_factory = sqlite3.Row
        DB['conn'] = c
        DB['cursor'] = c.cursor()
        logging.info(f'Conectado ao banco de dados: {DB_FILE}')
        
        # Testa se a conexão funcionou
        DB['cursor'].execute("SELECT 1").fetchone()
        logging.info('Banco de dados OK!')
    except Exception as e:
        logging.error(f'Erro ao conectar ao banco: {e}')
        raise

def execute(sql, args=None):
    global DB
    sql = re.sub(r'\s+', ' ', sql).strip()
    logging.info(f'SQL: {sql} Args: {args}')
    try:
        if args:
            return DB['cursor'].execute(sql, args)
        else:
            return DB['cursor'].execute(sql)
    except Exception as e:
        logging.error(f'Erro na consulta SQL: {e}')
        raise

def close():
    global DB
    if DB.get('conn'):
        DB['conn'].close()
        logging.info('Conexão com banco fechada')
