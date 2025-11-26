from flask import render_template, request, redirect, session, flash, url_for, Blueprint
from models import Usuarios
from helpers import  FormularioUsuario
from routes_game import rotas



@rotas.route('/login')
def login():
    proxima = request.args.get('proxima') #essa variavel guardar o valor: "/novo"
    form = FormularioUsuario()
    return render_template('login.html', proxima=proxima, form=form)


@rotas.route('/autenticar', methods=['POST'])
def autenticar():
    form = FormularioUsuario(request.form)
    usuario = Usuarios.query.filter_by(nickname=form.nickname.data).first()
    if usuario:
        if form.senha.data == usuario.senha:
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
    

@rotas.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('rotas.index'))

    