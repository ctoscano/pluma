from django.core.urlresolvers import reverse
from pluma.models import User
from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY, load_backend

def get_user(request):
    from django.contrib.auth.models import AnonymousUser
    try:
        user_id = request.session[SESSION_KEY]
        backend_path = request.session[BACKEND_SESSION_KEY]
        backend = load_backend(backend_path)
        user = backend.get_user(user_id) or AnonymousUser()
    except KeyError:
        user = AnonymousUser()
    return user

class Context(object):

    def __init__(self, request):
        self.__request = request
        self.__user = None
        
    def get_url(self, controller, *args, **kwargs):
        return self.__request.build_absolute_uri(reverse(controller, args=args, kwargs=kwargs))
    
    @property
    def request(self):
        return self.__request
    
    @property
    def user(self):
        if self.__user is None:
            self.__user = get_user(self.request)
        return self.__user
    
