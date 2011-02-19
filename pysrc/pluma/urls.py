from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from pluma.controllers import app

urlpatterns = patterns('',
    # Example:
    # (r'^pluma/', include('pluma.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
    
    url(r'^$', app.index, name='home'),
    url(r'inbox', app.inbox, name='inbox'),
    url(r'edit/(?P<id>.*)', app.compose, name='edit'),
    url(r'compose', app.compose, name='compose'),
    url(r'p/(?P<id>.*)', app.doc, name='doc'),
    url(r'd/(?P<id>.*)', app.draft, name='draft'),
    url(r'drafts', app.drafts, name='drafts'),
    url(r'signup', app.signup, name='signup'),
    url(r'signin', app.signin, name='signin'),
    url(r'signout', app.signout, name='signout'),
    url(r'profile', app._404, name='profile'),
    url(r'(?P<uri>.*)', app.doc_in_domain, name='doc_in_domain'),
)
