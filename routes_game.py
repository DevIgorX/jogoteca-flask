from flask import render_template, request, redirect, session, flash, url_for, Blueprint, current_app , send_from_directory
from models import Jogos
from extension import db
from helpers import recupera_imagem, deletar_arquivo, FormularioJogo
import time


rotas = Blueprint('rotas',__name__)


@rotas.route('/')
def index():
    lista = Jogos.query.order_by(Jogos.id)
    # recupera_imagem=recupera_imagem NO FINAL DA LINHA ABAIXO
    return render_template('lista.html', titulo='Jogos', jogos=lista, recupera_imagem=recupera_imagem)

@rotas.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('rotas.login', proxima=url_for('rotas.novo'))) #proxima=url_for('novo') esse paramentro, vai virar uma query string na URL do login, exemplo: /login?proxima=/novo
    
    form = FormularioJogo()
    return render_template('novo.html', titulo='Novo Jogo', form=form)

@rotas.route('/criar', methods=['POST',])
def criar():
    form = FormularioJogo(request.form) #para capturar as informações que está sendo enviada no formulario

    if not form.validate_on_submit(): #retorna true ou false dependedo se o formulario estará validado ou não 
      return redirect(url_for('rotas.novo'))
    
    nome = form.nome.data #quando usamos a propriedade "data" queremos acessar o valor do input
    categoria = form.categoria.data
    console = form.console.data


    
    
    jogo = Jogos.query.filter_by(nome=nome).first() #verificar se o jogo existe e o salva na variavel jogo

    if jogo:
        flash('jogo já existente!')
        return redirect(url_for('rotas.index'))
    

    novo_jogo = Jogos(nome=nome, categoria=categoria, console=console) # type: ignore
    db.session.add(novo_jogo)
    db.session.commit()

    arquivo = request.files['arquivo']
    upload_path = current_app.config['UPLOAD_PATH']
    timestamp = time.time()
    arquivo.save(f'{upload_path}/capa{novo_jogo.id}-{timestamp}.jpg')

    return redirect(url_for('rotas.index'))



@rotas.route('/editar/<int:id>')
def editar(id):
    
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('rotas.login', proxima=url_for('rotas.editar')))
    
    jogo = Jogos.query.filter_by(id=id).first()

    form = FormularioJogo()
    form.nome.data = jogo.nome  # type: ignore
    form.categoria.data = jogo.categoria # type: ignore
    form.console.data = jogo.console  # type: ignore

    capa_jogo = recupera_imagem(id)
    return render_template('editar.html', titulo='Editando Jogo', id=id, capa_jogo=capa_jogo, form=form)


@rotas.route('/atualizar', methods=['POST'])
def atualizar():
   
   form = FormularioJogo()

   if form.validate_on_submit():
   
    jogo = Jogos.query.filter_by(id=request.form['id']).first()

    jogo.nome = form.nome.data # type: ignore
    jogo.categoria = form.categoria.data # type: ignore
    jogo.console = form.console.data # type: ignore
    db.session.add(jogo)
    db.session.commit()
 
    arquivo = request.files['arquivo']
    upload_path = current_app.config['UPLOAD_PATH']
    timestamp = time.time()
    deletar_arquivo(jogo.id) # type: ignore
    arquivo.save(f'{upload_path}/capa{jogo.id}-{timestamp}.jpg') # type: ignore


   return redirect(url_for('rotas.index'))

@rotas.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('rotas.login'))
    
    Jogos.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Jogo Deletado!')
    return redirect(url_for('rotas.index'))


@rotas.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo) #pega a imagem no diretorio e retorna, no caso pega a imagem do coputador e envia para a tela do usuario

