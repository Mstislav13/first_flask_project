from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    """
    класс - Форма поста
    """
    title = StringField('Заголовок', validators=[DataRequired()])
    description = TextAreaField('Краткое описание',
                                validators=[DataRequired()])
    content = TextAreaField('Текст', validators=[DataRequired()])
    submit = SubmitField('Сохранить')
