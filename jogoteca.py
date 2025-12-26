from flask import Flask
from extension import db
from routes_game import rotas
import routes_user
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt

app = Flask(__name__) #passamos __name__ para que o flask saiba onde está o módulo principal da aplicação
app.config.from_pyfile('config.py')
db.init_app(app)
crsf = CSRFProtect(app)
bcrypt = Bcrypt(app)
app.register_blueprint(rotas)


if __name__ == '__main__':
 app.run(debug=True)