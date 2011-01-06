from django.core.urlresolvers import reverse
from pluma.models import User
from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY, load_backend, get_user

class Context(object):

    def __init__(self, request):
        self.__request = request
        
    def get_url(self, controller, *args, **kwargs):
        return self.__request.build_absolute_uri(reverse(controller, args=args, kwargs=kwargs))
    
    @property
    def request(self):
        return self.__request
    
    @property
    def user(self):
        return self.request.user
    
