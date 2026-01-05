from flask import render_template, request, redirect, session, flash, url_for
from models import Usuarios
from helpers import  FormularioUsuario, FormularioCadastro
from routes_game import rotas
from flask_bcrypt import check_password_hash , generate_password_hash
from extension import db



@rotas.route('/login')
def login():
    proxima = request.args.get('proxima') #essa variavel guardar o valor: "/novo"
    form = FormularioUsuario()
    return render_template('login.html', proxima=proxima, form=form)


@rotas.route('/autenticar', methods=['POST'])
def autenticar():
    form = FormularioUsuario(request.form)
    usuario = Usuarios.query.filter_by(nickname=form.nickname.data).first()
    
    
    senha = check_password_hash(usuario.senha, form.senha.data) if usuario else False

    if usuario and senha:
        session['usuario_logado'] = usuario.nickname
        flash(usuario.nickname + ' logado com sucesso!')
        
        proxima_pagina = request.form['proxima']
        
        
        if proxima_pagina and proxima_pagina != 'None':
            return redirect(proxima_pagina)
        else:
            
            return redirect(url_for('rotas.index'))
            
    else:
        flash('Usuário ou senha incorretos.')
        return redirect(url_for('rotas.login'))
    

@rotas.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('rotas.index'))


@rotas.route('/cadastrar')
def cadastrar():
    form = FormularioCadastro()
    return render_template('cadastrar.html', form=form)

@rotas.route('/registrar', methods=['POST'])
def registrar():

    form = FormularioCadastro(request.form)

    if not form.validate_on_submit():
        return redirect(url_for('rotas.cadastrar'))
    

    nome = form.nome.data
    nickname = form.nickname.data
    senha = form.senha.data
    
    usuario = Usuarios.query.filter_by(nickname=nickname).first()

    if usuario:
        flash('já existe usuario com esse nickname, tente novamente!')
        return redirect(url_for('rotas.cadastrar'))

    senha_criptografada = generate_password_hash(senha).decode('utf-8')


    novo_usuario = Usuarios(nickname=nickname, nome=nome, senha=senha_criptografada) #type: ignore
    db.session.add(novo_usuario)
    db.session.commit()

    flash('Usuario Cadastrado com Sucesso!')
    return redirect(url_for('rotas.index'))