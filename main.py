# -*- coding: utf-8 -*-
from wsgiref.simple_server import make_server

import core
from templates import render
from core import Application
from models import TrainingSite
from logging_mod import Logger

# Создание копирование курса, список курсов
# Регистрация пользователя, список пользователей
# Логирование
from views import head_view

site = TrainingSite()
logger = Logger('main')


def main_view(request):
    logger.log('Список курсов')
    return '200 OK', render('course_list.html', objects_list=site.courses)


def create_course(request):
    if request['method'] == 'POST':
        # метод пост
        data = request['data']
        name = data['name']
        name = Application.decode_value(name)
        category_id = data.get('category_id')
        category = None
        if category_id:
            category = site.find_category_by_id(int(category_id))

            course = site.create_course('record', name, category)
            site.courses.append(course)
        # редирект?
        # return '302 Moved Temporarily', render('create_course.html')
        # Для начала можно без него
        return '200 OK', render('create_course.html')
    else:
        categories = site.categories
        return '200 OK', render('create_course.html', categories=categories)


def create_category(request):
    if request['method'] == 'POST':
        # метод пост
        data = request['data']
        # print(data)
        name = data['name']

        name = Application.decode_value(name)
        category_id = data.get('category_id')

        category = None
        if category_id:
            category = site.find_category_by_id(int(category_id))

        new_category = site.create_category(name, category)

        site.categories.append(new_category)
        # редирект?
        # return '302 Moved Temporarily', render('create_course.html')
        # Для начала можно без него
        return '200 OK', render('create_category.html')
    else:
        categories = site.categories
        return '200 OK', render('create_category.html', categories=categories)


def copy_course(request):
    request_params = request['request_params']
    # print(request_params)
    name = request_params['name']
    old_course = site.get_course(name)
    if old_course:
        new_name = 'copy_' + name
        new_course = old_course.clone()
        new_course.name = new_name
        site.courses.append(new_course)

    return '200 OK', render('course_list.html', objects_list=site.courses)


def category_list(request):
    logger.log('Список категорий')
    return '200 OK', render('category_list.html', objects_list=site.categories)


def about_view(request):
    result = {
        "secret": request.get('secret_key'),
        "key": request.get('key')
    }
    return '200 OK', render('about.html', secret=result)


def contact_view(request):
    # Проверка метода запроса
    if request['method'] == 'POST':
        print(request)
        data = request['data']
        title = data['title']
        title = core.Application.decode_value(title)
        text = data['text']
        text = core.Application.decode_value(text)
        email = str(data['email'])
        print('Нам пришло сообщение от ' + email + ' с темой ' + title + ' и текстом ' + text)
        return '200 OK', render('contact.html')
    else:
        return '200 OK', render('contact.html')


urlpatterns = {
    '/': main_view,
    '/create-course/': create_course,
    '/create-category/': create_category,
    '/copy-course/': copy_course,
    '/category-list/': category_list,
    '/about/': about_view,
    '/contact/': contact_view,
    "/head/": head_view

}


def secret_controller(request):
    request['secret'] = 'secret'


front_controllers = [
    secret_controller
]

application = Application(urlpatterns, front_controllers)
with make_server('', 8000, application) as httpd:
    print("Serving on port 8000...")
    httpd.serve_forever()