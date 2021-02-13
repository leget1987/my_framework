# -*- coding: utf-8 -*-
from views import not_found_404


class Application:
    def __init__(self, routes, fronts):
        self.routes = routes
        self.fronts = fronts

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        # если в конце зопроса не /, то добавим его
        if path[-1] != '/':
            path = path + '/'
        if path in self.routes:
            view = self.routes[path]
        else:
            view = not_found_404
        request = {}
        for front in self.fronts:
            front(request)
        code, body = view(request)
        start_response(code, [('ContexType', 'text/html')])
        return [body.encode('utf-8')]
