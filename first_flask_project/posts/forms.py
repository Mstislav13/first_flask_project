from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed


class PostForm(FlaskForm):
    """
    класс - Форма поста
    """
    title = StringField('Заголовок', validators=[DataRequired()])
    description = TextAreaField('Краткое описание',
                                validators=[DataRequired()])
    content = TextAreaField('Текст', validators=[DataRequired()])
    picture = FileField('Изображение к посту',
                        validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Сохранить')


class CommentForm(FlaskForm):
    """
    класс - Форма комментария
    """
    comment = StringField('Комментарий', validators=[DataRequired()])
