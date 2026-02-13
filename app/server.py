#! /usr/bin/python3
import logging
import os
from app import APP
import db

logging.basicConfig(level=logging.INFO,
                  format='%(asctime)s - %(levelname)s - %(message)s',
                  datefmt='%Y-%m-%d %H:%M:%S')
db.connect()

port = int(os.environ.get("PORT", 10000))

if __name__ == '__main__':
    
    APP.run(host='0.0.0.0', port=port)
