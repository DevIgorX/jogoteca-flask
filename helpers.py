import os 
from flask import current_app


def recupera_imagem(id):
    for nome_arquivo  in os.listdir(current_app.config['UPLOAD_PATH']):
     if f'capa{id}' in nome_arquivo:
         return nome_arquivo     
     
    return 'capa_padrao.png'


def deletar_arquivo(id):
   arquivo = recupera_imagem(id)
   if arquivo != 'capa_padrao.png':
    caminho_upload = current_app.config['UPLOAD_PATH']
    os.remove(os.path.join(caminho_upload, arquivo))