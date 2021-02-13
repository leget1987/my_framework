# -*- coding: utf-8 -*-
import quopri

from my_framework.templates import render


def main_view(request):
    result = {
        "secret": request.get('secret_key'),
        "key": request.get('key')
    }
    return '200 OK', render('index.html', secret=result)


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
        title = str(data['title'])
        text = str(data['text'])
        email = str(data['email'])
        print('Нам пришло сообщение от ' + email + ' с темой ' + title + ' и текстом ' + text)
        return '200 OK', render('contact.html')
    else:
        return '200 OK', render('contact.html')


def not_found_404(request):
    result = {
        "secret": request.get('secret_key'),
        "key": request.get('key')
    }
    return '404 not found', render('404_not_found.html', secret=result)
