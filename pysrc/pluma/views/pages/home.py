'''
Created on Nov 24, 2010

@author: ctoscano
'''
from pluma.views.pages import Page
from pluma.views.language import ukgettext as _
from slique.html.html import new
from slique.html.table import VerticalTable

class Home(Page):
    
    def __init__(self, context, contributions):
        self.contributions = contributions
        super(Home, self).__init__(context, _('title_home'))

        if self.c.user.is_authenticated():
            self.body.add('hello %s ' % self.c.user.username)
            self.body.add(new.a(href=self.c.get_url('inbox')
                                ).add('Inbox'))
            self.body.add(new.a(href=self.c.get_url('compose')
                            ).add('compose'))
            self.body.add(new.a(href=self.c.get_url('drafts')
                            ).add('drafts'))
            self.body.add(new.a(href=self.c.get_url('signout')
                            ).add('Sign Out'))
        else:
            self.body.add(new.a(href=self.c.get_url('signup')
                            ).add('Sign Up'))
            self.body.add(new.a(href=self.c.get_url('signin')
                            ).add('Sign In'))
        
        table = VerticalTable()
        self.body.add(table)
        
        for doc in self.contributions:
            p = new.p
            table.add(p)
            a = new.a(href=self.c.get_url('doc', id=doc.contribution)).add(doc.title)
            p.add(a)
            p.add(' (')
            a = new.a(href=self.c.get_url('edit', id=doc.contribution)).add('edit')
            p.add(a)
            p.add(') ')
        