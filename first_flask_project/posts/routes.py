from flask import (render_template, url_for, flash, redirect, request, abort,
                   Blueprint)
from flask_login import current_user, login_required
from first_flask_project import db
from first_flask_project.models import Post, Comment
from first_flask_project.posts.forms import PostForm, CommentForm
from first_flask_project.posts.utils import save_picture

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
    if request.method == 'POST':
        if form.picture.data:
            picture_name = save_picture(form.picture.data)
    if form.validate_on_submit():
        post = Post(title=form.title.data, description=form.description.data,
                    content=form.content.data, author=current_user,
                    image_file=None)
        db.session.add(post)
        db.session.commit()
        flash('Ваш пост создан!', 'success')
        return redirect(url_for('posts.allpost'))
    return render_template('create_post.html',
                           title='Новый пост', image_file=form.picture.data,
                           form=form, legend='Новый пост')


@posts.route("/post/<int:post_id>", methods=['GET', 'POST'])
def post(post_id):
    """
    Статья
    :param post_id:
    :return:
    """
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(content=form.comment.data, post_id=post_id,
                          username=current_user.username)
        db.session.add(comment)
        db.session.commit()
        flash('Ваш комментарий был создан.', 'success')
        return redirect(request.url)

    return render_template('post.html', title=post.title, post=post, form=form)


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
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            post.image_file = picture_file
        db.session.commit()
        flash('Ваш пост обновлен!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.description.data = post.description
        form.content.data = post.content
        image_file = url_for('static', filename='posts_img/' +
                                                post.image_file)
    return render_template('update_post.html', form=form,
                           image_file=image_file,
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


@posts.route("/comment/<int:comment_id>/delete", methods=['POST'])
@login_required
def delete_comment(comment_id):
    """
    Удаление комментария
    :param comment_id:
    :return:
    """
    comment = Comment.query.get_or_404(comment_id)
    if comment.username != current_user.username:
        abort(403)
    db.session.delete(comment)
    db.session.commit()
    flash('Ваш комментарий был удален!', 'success')
    return redirect(url_for('posts.allpost'))
