# -*- coding: utf-8 -*-
import sys
sys.path.append("..")

from wsgiref.util import setup_testing_defaults

from views import not_found_404
import quopri


class Application:
    #@staticmethod
    def decode_value(val):
        val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = quopri.decodestring(val_b)
        print(val_decode_str.decode('UTF-8'))
        return val_decode_str.decode('UTF-8')

    def add_route(self, url):
        # паттерн декоратор
        def inner(view):
            self.routes[url] = view

        return inner

    def parse_input_data(self, data):
        result = {}
        if data:
            params = data.split('&')

            for item in params:
                k, v = item.split('=')
                result[k] = v
        return result

    def parse_wsgi_input_data(self, data):
        result = {}
        if data:
            data_str = data.decode(encoding='utf-8')
            result = self.parse_input_data(data_str)
        return result

    def get_wsgi_input_data(self, environ):
        content_length_data = environ.get('CONTENT_LENGTH')
        content_length = int(content_length_data) if content_length_data else 0
        data = environ['wsgi.input'].read(content_length) if content_length > 0 else b''
        return data

    def __init__(self, routes, fronts):
        self.routes = routes
        self.fronts = fronts

    def __call__(self, environ, start_response):
        print(self.routes)
        setup_testing_defaults(environ)
        path = environ['PATH_INFO']
        print(path)
        method = environ['REQUEST_METHOD']
        data = self.get_wsgi_input_data(environ)
        data = self.parse_wsgi_input_data(data)
        query_string = environ['QUERY_STRING']
        request_params = self.parse_input_data(query_string)
        print(request_params)
        # если в конце зопроса нет /, то добавим его
        if path[-1] != '/':
            path = path + '/'
        if path in self.routes:
            view = self.routes[path]
            request = dict()
            # добавляем параметры запросов
            request['method'] = method
            request['data'] = data
            request['request_params'] = request_params
            for front in self.fronts:
                front(request)
            code, body = view(request)
            start_response(code, [('ContexType', 'text/html')])
            return [body.encode('utf-8')]
        else:
            view = not_found_404
            request = dict()
            code, body = view(request)
            start_response(code, [('ContexType', 'text/html')])
            return [body.encode('utf-8')]


# Новый вид WSGI-application.
# Первый — логирующий (такой же, как основной,
# только для каждого запроса выводит информацию
# (тип запроса и параметры) в консоль.
class DebugApplication(Application):

    def __init__(self, urlpatterns, front_controllers):
        self.application = Application(urlpatterns, front_controllers)
        super().__init__(urlpatterns, front_controllers)

    def __call__(self, env, start_response):
        print('DEBUG MODE')
        print(env)
        return self.application(env, start_response)


# Новый вид WSGI-application.
# Второй — фейковый (на все запросы пользователя отвечает:
# 200 OK, Hello from Fake).
class FakeApplication(Application):

    def __init__(self, urlpatterns, front_controllers):
        self.application = Application(urlpatterns, front_controllers)
        super().__init__(urlpatterns, front_controllers)

    def __call__(self, env, start_response):
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [b'Hello from Fake']
