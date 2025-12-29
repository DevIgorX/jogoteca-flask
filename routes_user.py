from flask import render_template, request, redirect, session, flash, url_for
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
<<<<<<< HEAD

    # Verifica se o usuário existe antes de checar a senha
    senha = check_password_hash(usuario.senha, form.senha.data) if usuario else False #if ternário (valor_se_sim if condição else valor_se_não)

        #codigo equivalente

#    if usuario:
#     senha = check_password_hash(usuario.senha, form.senha.data)
#    else:
#     senha = False
=======
    
    
    senha = check_password_hash(usuario.senha, form.senha.data) if usuario else False
>>>>>>> 8e200e4dd8a5640ed5c6d4435c0792f9998c1262

    if usuario and senha:
        session['usuario_logado'] = usuario.nickname
        flash(usuario.nickname + ' logado com sucesso!')
        
        proxima_pagina = request.form['proxima']
        
        
        if proxima_pagina and proxima_pagina != 'None':
            return redirect(proxima_pagina)
        else:
<<<<<<< HEAD
            # Se não tiver próxima página, vai para o início (index)-
=======
            
>>>>>>> 8e200e4dd8a5640ed5c6d4435c0792f9998c1262
            return redirect(url_for('rotas.index'))
            
    else:
        flash('Usuário ou senha incorretos.')
        return redirect(url_for('rotas.login'))
    

@rotas.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('rotas.index'))


    