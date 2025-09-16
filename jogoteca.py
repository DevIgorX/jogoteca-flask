from flask import Flask
from extension import db
from routes import rotas

app = Flask(__name__)
app.config.from_pyfile('config.py')
db.init_app(app)
app.register_blueprint(rotas)

if __name__ == '__main__':
 app.run(debug=True)