from flask import render_template, request, redirect, session, flash, url_for, Blueprint, jsonify
from models import Jogos, Usuarios
from extension import db


rotas = Blueprint('rotas',__name__)

@rotas.route('/')
def index():
    lista = Jogos.query.order_by(Jogos.id)
    return render_template('lista.html', titulo='Jogos', jogos=lista)

@rotas.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo'))) #proxima=url_for('novo') esse paramentro, vai virar uma query string na URL do login, exemplo: /login?proxima=/novo
    return render_template('novo.html', titulo='Novo Jogo')

@rotas.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    
    jogo = Jogos.query.filter_by(nome=nome).first()

    if jogo:
        flash('jogo já existente!')
        return redirect(url_for('rotas.index'))
    

    novo_jogo = Jogos(nome=nome, categoria=categoria, console=console) # type: ignore
    db.session.add(novo_jogo)
    db.session.commit()

    return redirect(url_for('rotas.index'))

@rotas.route('/login')
def login():
    proxima = request.args.get('proxima') #essa variavel guardar o valor: "/novo"
    return render_template('login.html', proxima=proxima)


@rotas.route('/autenticar', methods=['POST'])
def autenticar():
    usuario = Usuarios.query.filter_by(nickaname=request.form['usuario']).first()
    if usuario:
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ' logado com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
        else:
            flash('Senha incorreta.')
            return redirect(url_for('rotas.login'))
    else:
        flash('Usuário não logado.')
        return redirect(url_for('rotas.login'))
    


@rotas.route('/editar')
def editar():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar')))
    return render_template('editar.html', titulo='Editando Jogo')


@rotas.route('/atualizar', methods=['POST'])
def atualizar():
   return redirect(url_for('rotas.index'))


@rotas.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('rotas.index'))