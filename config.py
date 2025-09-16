
import os

# Pega o caminho absoluto para o diretório onde este arquivo (config.py) está.
basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = 'alura'

# Cria o caminho absoluto para o arquivo do banco de dados dentro do diretório do projeto.
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'jogoteca.db')