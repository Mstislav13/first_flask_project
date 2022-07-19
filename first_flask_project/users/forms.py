from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, \
    ValidationError
from flask_login import current_user
from first_flask_project.models import User


class RegistrationForm(FlaskForm):
    """
    класс - Форма регистрации пользователя
    """
    username = StringField('Имя пользователя:',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email:', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль:', validators=[DataRequired()])
    confirm_password = PasswordField('Подтвердить пароль:',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        """
        Проверка username
        :param username:
        :return:
        """
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'Это имя занято. Пожалуйста, выберите другое.')

    def validate_email(self, email):
        """
        Проверка email
        :param email:
        :return:
        """
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'Этот email занят. Пожалуйста, выберите другой.')


class LoginForm(FlaskForm):
    """
    класс - LoginForm (вход на сайт)
    """
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Напомнить пароль')
    submit = SubmitField('Войти')


class UpdateAccountForm(FlaskForm):
    """
    класс - Редактирование профиля пользователя
    """
    username = StringField('Имя пользователя',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Обновить аватар',
                        validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Обновить')

    def validate_username(self, username):
        """
        Проверка username
        :param username:
        :return:
        """
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Это имя занято. '
                                      'Пожалуйста, выберите другое')

    def validate_email(self, email):
        """
        Проверка email
        :param email:
        :return:
        """
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Этот email занят'
                                      'Пожалуйста, выберите другой')


class RequestResetForm(FlaskForm):
    """
    класс - Запрос на изменение пароля
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Изменить пароль')

    def validate_email(self, email):
        """
        Проверка email
        :param email:
        :return:
        """
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('Аккаунт с данным email-адресом '
                                  'отсутствует. '
                                  'Вы можете его зарегистрировать.')


class ResetPasswordForm(FlaskForm):
    """
    класс - Изменение пароля
    """
    password = PasswordField('Пароль:', validators=[DataRequired()])
    confirm_password = PasswordField('Подтвердите пароль:',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField('Изменить пароль')
