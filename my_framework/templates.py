# -*- coding: utf-8 -*-
from jinja2 import Template
import os


def render(template_name, folder='templates', **kwargs):
    """
    :param template_name: имя шаблона
    :param folder: папка в которой ищем шаблон
    :param kwargs: параметры
    :return:
    """
    file_path = os.path.join(folder, template_name)
    # Открываем шаблон по имени
    with open(file_path) as f:
        # Читаем
        template = Template(f.read())
    # рендерим шаблон с параметрами
    return template.render(**kwargs)


