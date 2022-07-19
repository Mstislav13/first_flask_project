from flask import (render_template, url_for, flash, redirect, request, abort,
                   Blueprint)
from flask_login import current_user, login_required
from first_flask_project import db
from first_flask_project.models import Post, Comments
from first_flask_project.posts.forms import PostForm

posts = Blueprint('posts', __name__)


@posts.route("/allpost")
@login_required
def allpost():
    """
    Все статьи
    :return:
    """
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.created.desc()).paginate(
        page=page, per_page=5)
    return render_template('allpost.html', posts=posts)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    """
    Создание новой статьи
    :return:
    """
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, description=form.description.data,
                    content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Ваш пост создан!', 'success')
        return redirect(url_for('posts.allpost'))
    return render_template('create_post.html',
                           title='Новый пост', form=form, legend='Новый пост')


@posts.route("/post/<int:post_id>", methods=['GET', 'POST'])
def post(post_id):
    """
    Статья
    :param post_id:
    :return:
    """
    post = Post.query.get_or_404(post_id)
    comment = Comments.query.filter_by(post_id=post.id).all()
    if request.method == 'POST':
        post_id = post.id
        name = request.form.get('name')
        email = request.form.get('email')
        content = request.form.get('content')
        comment = Comments(name=name, email=email, content=content,
                           post_id=post_id)
        db.session.add(comment)
        db.session.commit()
        flash('Ваш комментарий был создан.', 'success')
        return redirect(request.url)

    return render_template('post.html', title=post.title, post=post,
                           comment=comment)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    """
    Редактирование статьи
    :param post_id:
    :return:
    """
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.description = form.description.data
        post.content = form.content.data
        db.session.commit()
        flash('Ваш пост обновлен!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.description.data = post.description
        form.content.data = post.content
    return render_template('update_post.html', form=form,
                           legend='Редактирование поста')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    """
    Удаление статьи
    :param post_id:
    :return:
    """
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Ваш пост был удален!', 'success')
    return redirect(url_for('posts.allpost'))
