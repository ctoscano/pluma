'''
Created on Nov 24, 2010

@author: ctoscano
'''
from pluma.views.pages import Page
from pluma.views.language import ukgettext as _
from slique.html.html import new
from slique.html.table import VerticalTable
from pluma.views import csrf_token

class SignIn(Page):
    
    def __init__(self, context):
        super(SignIn, self).__init__(context, _('title_home'))

        form = new.form(method='POST')
        table = VerticalTable()
        form.add(table)
        self.body.add(form)
        
        table.add(csrf_token(self.c.request))
        table.add(new.input(name='username', value='username', type='text'))
        table.add(new.input(name='password', value='password', type='password'))
        table.add(new.button(type='submit').add(_('Sign In')))
