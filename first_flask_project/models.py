from datetime import datetime
from first_flask_project import db, login_manager
from flask_login import UserMixin


class User(db.Model, UserMixin):
    """
    класс - модель пользователя
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    avatar_image = db.Column(db.String(30), nullable=False,
                             default='default.png')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)


class Post(db.Model):
    """
    класс - модель статьи
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
