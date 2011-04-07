'''
Created on Nov 24, 2010

@author: ctoscano
'''
from pluma.views.pages import Page
from pluma.views.language import ukgettext as _
from slique.html.html import new
from slique.html.table import VerticalTable

class Inbox(Page):
    
    def __init__(self, context, contributions):
        self.contributions = contributions
        super(Inbox, self).__init__(context, _('title_home'))

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
        
    @property
    def left(self):
        if self._left is None:
            super(Inbox, self).left
            
            table = VerticalTable()
            self._left.add(table)
            table.add(new.a(href=self.c.get_url('inbox')
                                ).add('Inbox'))
            table.add(new.a(href=self.c.get_url('compose')
                            ).add('compose'))
            table.add(new.a(href=self.c.get_url('drafts')
                            ).add('drafts'))
        return self._left
