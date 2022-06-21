from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from first_flask_project.config import Config

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    """
    :return:
    """
    app = Flask(__name__)

    app.config.from_object(Config)
    login_manager.init_app(app)

    from first_flask_project.main.routes import main
    app.register_blueprint(main)

    return app
