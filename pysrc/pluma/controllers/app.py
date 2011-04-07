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
from pluma.views.pages.drafts import Drafts
from pluma.views.pages.inbox import Inbox

def index(request):
    c = Context(request)
    if c.user.is_anonymous():
        page = Home(c, [])
    else:
        page = Inbox(c, c.user.get_inbox())
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
def drafts(request):
    c = Context(request)
    page = Drafts(c, Draft.get_user_drafts(c.user))
    return HttpResponse(page)

@login_required
def draft(request, id):
    c = Context(request)
    draft = Draft.with_id(c.user, id)
    return compose(request, 
                   draft.contribution if hasattr(draft, 'contribution') else None, 
                   draft, 
                   c)

@login_required
def compose(request, id=None, draft=None, c=None):
    c = c or Context(request)
    
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
        contrib.set_url(c.request.POST.get('domain', False),
                        c.request.POST.get('uri', False))
        contrib.mode = c.request.POST.get('type', False) or contrib.mode or 'plain'
        if c.request.POST.get('save', False): # Save draft
            if hasattr(contrib, '_id'):       # Editing contribution's draft
                Draft.save_draft(c.user, contrib)
            else: # There is no contribution associated with this draft 
                if draft:               # modify existing draft
                    draft.content = c.request.POST.get('content')
                    draft.title = c.request.POST.get('title')
                    draft.save()
                else: 
                    draft = Draft()     # Saving new draft
                    draft.set_user(c.user)
                    draft.content = c.request.POST.get('content')
                    draft.title = c.request.POST.get('title')
                    draft.save(force_insert=True)
                    draft_url = c.get_url('draft', id=draft[draft._meta['id_field']])
                    return HttpResponseRedirect(draft_url)        
        elif c.request.POST.get('discard', False):      # Discard draft
            Draft.remove(user=c.user, contrib=contrib, draft=draft)
            return HttpResponseRedirect('/')
        else:
            contrib.save()                              # Save Version
            Draft.remove(c.user, contrib)
            return HttpResponseRedirect('/')
    elif draft:
        contrib.title = draft.title                 # Not POSTING new info,  
        contrib.set_text(draft.content)             # but editing draft

    return HttpResponse(Compose(c, contrib))

def doc(request, id, domain=None, uri=None):
    c = Context(request)
    doc = Contribution.factory(id, domain=domain, uri=uri)
    if doc:
        return HttpResponse(doc.rendered_content, content_type=doc.content_type)
    else: 
        return _404(request)

def doc_in_domain(request, uri):
    '''same as doc, but filters documents associated with a specific domain
    '''
    domain = request.META['SERVER_NAME']
    return doc(request, None, domain, uri)

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

@login_required
def inbox(request):
    return index(request)

def _404(request):
    return HttpResponse('not found', status=404)
