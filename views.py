from my_framework.templates import render


def main_view(request):
    result = {
        "secret": request.get('secret_key'),
        "key": request.get('key')
    }
    return '200 OK', render('index.html', secret=result)


def about_view(request):
    secret = request.get('secret_key', None)
    return '200 OK', render('about.html', secret=secret)


def not_found_404(request):
    secret = request.get('secret_key', 'key')
    return '404 not found', render('404_not_found.html', secret=secret)

