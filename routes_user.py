from flask import render_template, request, redirect, session, flash, url_for, Blueprint
from models import Usuarios
from helpers import  FormularioUsuario
from routes_game import rotas
from flask_bcrypt import check_password_hash



@rotas.route('/login')
def login():
    proxima = request.args.get('proxima') #essa variavel guardar o valor: "/novo"
    form = FormularioUsuario()
    return render_template('login.html', proxima=proxima, form=form)


@rotas.route('/autenticar', methods=['POST'])
def autenticar():
    form = FormularioUsuario(request.form)
    usuario = Usuarios.query.filter_by(nickname=form.nickname.data).first()
    
    # Verifica se o usuário existe antes de checar a senha ---
    senha = check_password_hash(usuario.senha, form.senha.data) if usuario else False

    if usuario and senha:
        session['usuario_logado'] = usuario.nickname
        flash(usuario.nickname + ' logado com sucesso!')
        
        proxima_pagina = request.form['proxima']
        
        # AQUI ESTÁ A CORREÇÃO PRINCIPAL:
        # Verificamos se proxima_pagina não é a palavra 'None'
        if proxima_pagina and proxima_pagina != 'None':
            return redirect(proxima_pagina)
        else:
            # Se não tiver próxima página, vai para o início (index)
            return redirect(url_for('rotas.index'))
            
    else:
        flash('Usuário ou senha incorretos.')
        return redirect(url_for('rotas.login'))
    

@rotas.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('rotas.index'))

    