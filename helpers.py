import os 
from flask import current_app


def recupera_imagem(id):
    for nome_arquivo  in os.listdir(current_app.config['UPLOAD_PATH']):
     if f'capa{id}' in nome_arquivo:
         return nome_arquivo     
     
    return 'capa_padrao.png'