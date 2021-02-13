from my_framework.core import Application
import views

urlpatterns = {
    '/': views.main_view,
    '/about/': views.about_view,
    '/contact/': views.contact_view
}


def secret_controller(request):
    request['secret_key'] = 'SECRET'


def secret_key(request):
    request['key'] = 'KEY'


front_controllers = [secret_controller, secret_key]
application = Application(urlpatterns, front_controllers)
