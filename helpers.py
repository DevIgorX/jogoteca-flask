import os 
from flask import current_app
from flask_wtf import FlaskForm #flask-wtf serve para integrar o flask com o wtformss
from wtforms import StringField, validators, SubmitField #campos + validadores


class FormularioJogo(FlaskForm):
   nome = StringField('Nome do jogo',[validators.DataRequired(), validators.length(min=1, max=50)])
   categoria = StringField('Categoria',[validators.DataRequired(), validators.length(min=1, max=40)])
   console = StringField('Console',[validators.DataRequired(), validators.length(min=1, max=20)])
   salvar = SubmitField('Salvar')


def recupera_imagem(id):
    for nome_arquivo  in os.listdir(current_app.config['UPLOAD_PATH']):
     if f'capa{id}' in nome_arquivo:
         return nome_arquivo     
     
    return 'capa_padrao.png'


def deletar_arquivo(id):
   arquivo = recupera_imagem(id)
   if arquivo != 'capa_padrao.png':
    caminho_upload = current_app.config['UPLOAD_PATH']
    os.remove(os.path.join(caminho_upload, arquivo)) #