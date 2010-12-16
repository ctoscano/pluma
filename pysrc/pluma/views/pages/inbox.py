'''
Created on Nov 24, 2010

@author: ctoscano
'''
from pluma.views.pages import Page
from pluma.views.language import ukgettext as _
from slique.html.html import new
from slique.html.table import VerticalTable

class Ledger(Page):
    
    def __init__(self, context, contributions):
        self.contributions = contributions
        super(Ledger, self).__init__(context, _('title_home'))

        self.body.add(new.a(href=self.c.get_url('compose')
                            ).add('compose'))
        self.body.add(new.a(href=self.c.get_url('signout')
                            ).add('Sign Out'))
        
        table = VerticalTable()
        self.body.add(table)
        
        for doc in self.contributions:
            p = new.p
            table.add(p)
            a = new.a(href=self.c.get_url('doc', id=doc._id)).add(doc.title)
            p.add(a)
            p.add(' (')
            a = new.a(href=self.c.get_url('edit', id=doc._id)).add('edit')
            p.add(a)
            p.add(') ')
        