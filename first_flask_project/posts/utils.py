import os
from secrets import token_hex
from PIL import Image
from flask import current_app


def save_picture(form_picture):
    """
    Сохранение картинок к посту
    :param form_picture:
    :return:
    """
    random_hex = token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/posts_img',
                                picture_fn)
    output_size = (300, 300)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn
