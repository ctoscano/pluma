'''
Created on Nov 24, 2010

@author: ctoscano
'''
from django.http import HttpResponse, HttpResponseRedirect
from pluma.controllers import Context
from pluma.views.pages.home import Home
from pluma.views.pages.compose import Compose
from pluma.models import Contribution, User, Draft
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
            return _404(request)
    else:   
        #TODO: validate 'type' 
        contrib = Contribution.factory(type=c.request.POST.get('type', 'plain'))
        contrib.author = c.user
        contrib.add_accessor(c.user)
    
    if c.request.POST:
        contrib.title = c.request.POST.get('title')
        contrib.set_text(c.request.POST.get('content'))
        contrib.set_domain(c.request.POST.get('domain', False))
        if c.request.POST.get('save', False):           # Save draft
            Draft.save_draft(c.user, contrib)
        elif c.request.POST.get('discard', False):      # Discard draft
            Draft.remove(c.user, contrib)
            return HttpResponseRedirect('/')
        else:
            contrib.save()                              # Save Version
            Draft.remove(c.user, contrib)
            return HttpResponseRedirect('/')

    return HttpResponse(Compose(c, contrib))

def doc(request, id, domain=None):
    c = Context(request)
    doc = Contribution.factory(id, domain=domain)
    if doc:
        return HttpResponse(doc.rendered_content, content_type=doc.content_type)
    else: 
        return _404(request)

def doc_in_domain(request, id):
    '''same as doc, but filters documents associated with a specific domain
    '''
    domain = request.META['SERVER_NAME']
    return doc(request, id, domain)

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
            return HttpResponseRedirect(c.request.GET.get('next', '/'))
                
    return HttpResponse(SignIn(c))

def signout(request):
    logout(request)
    return HttpResponse('signed out')

def inbox(request):
    return index(request)

def _404(request):
    return HttpResponse('not found', status=404)
