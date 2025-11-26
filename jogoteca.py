from flask import Flask
from extension import db
from routes_game import rotas
from flask_wtf .csrf import CSRFProtect

app = Flask(__name__) #passamos __name__ para que o flask saiba onde está o módulo principal da aplicação
app.config.from_pyfile('config.py')
db.init_app(app)
crsf = CSRFProtect(app)
app.register_blueprint(rotas)


if __name__ == '__main__':
 app.run(debug=True)