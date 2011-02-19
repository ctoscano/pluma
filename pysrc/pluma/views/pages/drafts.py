'''
Created on Nov 24, 2010

@author: ctoscano
'''
from pluma.views.pages import Page
from pluma.views.language import ukgettext as _
from slique.html.html import new
from slique.html.table import VerticalTable

class Drafts(Page):
    
    def __init__(self, context, contributions):
        self.contributions = contributions
        super(Drafts, self).__init__(context, _('title_drafts'))

        self.body.add(new.a(href=self.c.get_url('inbox')
                            ).add('inbox'))
        self.body.add(new.a(href=self.c.get_url('signout')
                            ).add('Sign Out'))
        
        table = VerticalTable()
        self.body.add(table)
        
        for doc in self.contributions:
            p = new.p
            table.add(p)
            if hasattr(doc, 'contribution') and doc.contribution:
                url = self.c.get_url('edit', id=doc.contribution)
            else:
                url = self.c.get_url('draft', id=doc._id)
            a = new.a(href=url).add(doc.title)
            p.add(a)
        