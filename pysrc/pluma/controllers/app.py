'''
Created on Nov 24, 2010

@author: ctoscano
'''
from django.http import HttpResponse, HttpResponseRedirect
from pluma.controllers import Context
from pluma.views.pages.home import Home
from pluma.views.pages.compose import Compose
from pluma.models import Contribution, User
from pluma.views.pages.signup import SignUp
from django.contrib.auth import login, logout
from pluma.views.pages.signin import SignIn
from django.contrib.auth.decorators import login_required

def index(request):
    c = Context(request)
    
    page = Home(c, [] if c.user.is_anonymous() else c.user.get_inbox())
    return HttpResponse(page)

def info(request):
    page = Home(Context(request))

    from slique.html.table import VerticalTable
    table = VerticalTable()
    table.add(request.environ)
    table.nextRow()
    table.add(request.path_info)
    table.nextRow()
    table.add(request.path)
    
    page.body.add(table)
    return HttpResponse(page)

@login_required
def compose(request, id=None):
    c = Context(request)
    
    if id:  
        contrib = Contribution.factory(id)
        if not contrib: 
            return HttpResponse('not found', status=404)
    else:   
        #TODO: validate 'type' 
        contrib = Contribution.factory(type=c.request.POST.get('type', 'plain'))
        contrib.author = c.user
        contrib.add_accessor(c.user)
    
    if c.request.POST:
        contrib.title = c.request.POST.get('title')
        contrib.rendered_content = c.request.POST.get('content')
        contrib.save()
        return HttpResponseRedirect('/')
    
    return HttpResponse(Compose(c, contrib))

def doc(request, id):
    c = Context(request)
    doc = Contribution.factory(id)
    return HttpResponse(doc.rendered_content, content_type=doc.content_type) 

def signup(request):
    c = Context(request)
    if c.request.POST:
        # this user is a Auth_User object, not a Custom User object
        user = User.create_user(c.request.POST.get('username'),
                                c.request.POST.get('password'))
        return HttpResponse('signed up')
    return HttpResponse(SignUp(c))

def signin(request):
    c = Context(request)
    if c.request.POST:
        user = User.objects(username=c.request.POST.get('username')).first()
        if user and user.check_password(c.request.POST.get('password')):
            user.backend = 'mongoengine.django.auth.MongoEngineBackend'
            login(c.request, user)
            return HttpResponse('signed in')
    return HttpResponse(SignIn(c))

def signout(request):
    logout(request)
    return HttpResponse('signed out')

def inbox(request):
    c = Context(request)
    return HttpResponse('signed out')

