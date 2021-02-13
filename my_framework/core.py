# -*- coding: utf-8 -*-
from views import not_found_404


class Application:

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
        path = environ['PATH_INFO']
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
