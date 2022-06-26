from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from first_flask_project.config import Config
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()


def create_app():
    """
    Создание приложений
    :return:
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    from first_flask_project.main.routes import main
    from first_flask_project.users.routes import users
    app.register_blueprint(main)
    app.register_blueprint(users)

    return app
