from django.core.context_processors import csrf
from slique.html.element import element


class csrf_token(element):
    
    def __init__(self, request):
        super(csrf_token, self).__init__('input',
            name='csrfmiddlewaretoken',
            value=str(csrf(request)['csrf_token']),
            type='hidden')
