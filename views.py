# -*- coding: utf-8 -*-
from my_framework.templates import render


def head_view(request):
    result = {
        "secret": request.get('secret_key'),
        "key": request.get('key')
    }
    return '200 OK', render('index.html', secret=result)


def not_found_404(request):
    result = {
        "secret": request.get('secret_key'),
        "key": request.get('key')
    }
    return '404 not found', render('404_not_found.html', secret=result)
