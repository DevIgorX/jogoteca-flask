from flask import Flask
from extension import db
from routes_game import rotas
import routes_user
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt

app = Flask(__name__) #passamos __name__ para que o flask saiba onde está o módulo principal da aplicação e consegue localizar os outros arquivos do projeto, como se fosse uma instancia 
app.config.from_pyfile('config.py')
db.init_app(app) # inicializa passando a aplicação flask para dentro do sqlalchemy, precisa que as configurações já estejam carregadas 'config.py' dentro do app para saber o que fazer
crsf = CSRFProtect(app) # Ativa o proteção global contra ataques CSRF , o flask começa a exigir o token em formulários POST.
bcrypt = Bcrypt(app)
app.register_blueprint(rotas)


if __name__ == '__main__':
 app.run(debug=True)