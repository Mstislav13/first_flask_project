from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
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

    def get_reset_token(self, expires_sec=1800):
        """
        Получение токена для изменения пароля
        :param expires_sec:
        :return:
        """
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        """
        Проверка токена
        :param token:
        :return:
        """
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except Exception:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        """
        :return:
        """
        return f"Пользователь('{self.username}', " \
               f"'{self.email}', '{self.avatar_image}')"


class Post(db.Model):
    """
    класс - модель статьи
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    comments = db.relationship('Comment', backref='title', lazy='dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    image_file = db.Column(db.String(30), nullable=False,
                           default='default.png')

    def __repr__(self):
        """
        :return:
        """
        return f"Запись('{self.title}', '{self.created}')"


@login_manager.user_loader
def load_user(user_id):
    """
    Загрузка пользователя
    :param user_id:
    :return:
    """
    return User.query.get(int(user_id))


class Comment(db.Model):
    """
    класс - модель комментариев
    """
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(50), db.ForeignKey('user.username'),
                         nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'
                                                  ), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        """
        :return:
        """
        return f"Комментарий('{self.username}', '{self.content}')"
