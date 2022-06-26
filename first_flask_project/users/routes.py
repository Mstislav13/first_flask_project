from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from first_flask_project import db, bcrypt
from first_flask_project.models import User, Post
from first_flask_project.users.forms import RegistrationForm, LoginForm, \
    UpdateAccountForm, RequestResetForm, ResetPasswordForm
from first_flask_project.users.utils import save_picture

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    """
    Регистрация нового пользователя
    :return:
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Ваша учетная запись была создана!'
              ' Теперь вы можете войти в систему', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Регистрация', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    """
    Вход на сайт
    :return:
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,
                                               form.password.data):
            login_user(user, remember=form.remember.data)

            return redirect(url_for('main.home'))
        else:
            flash('Войти не удалось. Пожалуйста, '
                  'проверьте электронную почту и пароль', 'внимание')
    return render_template('login.html', title='Аутентификация', form=form)


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    """
    Вход в профиль пользователя
    :return:
    """
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.avatar_image = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Ваш аккаунт был обновлен!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        page = request.args.get('page', 1, type=int)
        user = User.query.filter_by(username=form.username.data).first_or_404()
        posts = Post.query.filter_by(author=user) \
            .order_by(Post.created.desc()) \
            .paginate(page=page, per_page=5)
    avatar_image = url_for('static', filename='profile_pics/' +
                                              current_user.avatar_image)
    return render_template('account.html', title='Аккаунт',
                           avatar_image=avatar_image, form=form, posts=posts,
                           user=user)


@users.route("/logout")
def logout():
    """
    Выход с сайта
    :return:
    """
    logout_user()
    return redirect(url_for('main.home'))
