from flask import render_template, request, redirect, session, flash, url_for, Blueprint, current_app , send_from_directory
from models import Jogos, Usuarios
from extension import db
from helpers import recupera_imagem, deletar_arquivo, FormularioJogo
import time



rotas = Blueprint('rotas',__name__)

@rotas.route('/')
def index():
    lista = Jogos.query.order_by(Jogos.id)
    return render_template('lista.html', titulo='Jogos', jogos=lista)

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
    
    nome = form.nome.data
    categoria = form.categoria.data
    console = form.console.data
    
    jogo = Jogos.query.filter_by(nome=nome).first()

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

@rotas.route('/login')
def login():
    proxima = request.args.get('proxima') #essa variavel guardar o valor: "/novo"
    return render_template('login.html', proxima=proxima)


@rotas.route('/autenticar', methods=['POST'])
def autenticar():
    usuario = Usuarios.query.filter_by(nickname=request.form['usuario']).first()
    if usuario:
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ' logado com sucesso!')
            proxima_pagina = request.form['proxima']
            if proxima_pagina:
             return redirect(proxima_pagina)
        
            return redirect(url_for('rotas.index'))
        else:
            flash('Senha incorreta.')
            return redirect(url_for('rotas.login'))
    else:
        flash('Usuário não logado.')
        return redirect(url_for('rotas.login'))
    


@rotas.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('rotas.login', proxima=url_for('rotas.editar')))
    jogo = Jogos.query.filter_by(id=id).first()
    capa_jogo = recupera_imagem(id)
    return render_template('editar.html', titulo='Editando Jogo', jogo=jogo, capa_jogo=capa_jogo)


@rotas.route('/atualizar', methods=['POST'])
def atualizar():
   
   jogo = Jogos.query.filter_by(id=request.form['id']).first()

   jogo.nome = request.form['nome'] # type: ignore
   jogo.categoria = request.form['categoria'] # type: ignore
   jogo.console = request.form['console'] # type: ignore

   db.session.add(jogo)
   db.session.commit()
 
   arquivo = request.files['arquivo']
   upload_path = current_app.config['UPLOAD_PATH']
   timestamp = time.time()
   deletar_arquivo(jogo.id)
   arquivo.save(f'{upload_path}/capa{jogo.id}-{timestamp}.jpg')


   return redirect(url_for('rotas.index'))

@rotas.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('rotas.login'))
    
    Jogos.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Jogo Deletado!')
    return redirect(url_for('rotas.index'))



@rotas.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('rotas.index'))

@rotas.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo) #pega a imagem no diretorio e retorna, no caso pega a imagem do coputador e envia para a tela do usuario

