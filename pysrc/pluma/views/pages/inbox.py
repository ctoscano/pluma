'''
Created on Nov 24, 2010

@author: ctoscano
'''
from pluma.views.pages import WorkPage
from pluma.views.language import ukgettext as _
from slique.html.html import new
from slique.html.table import VerticalTable

class Inbox(WorkPage):
    
    def __init__(self, context, contributions):
        self.contributions = contributions
        super(Inbox, self).__init__(context, _('title_home'))

    @property
    def center(self):
        if self._center is None:
            super(Inbox, self).center
            table = VerticalTable()
            self._center.add(table)
            
            for doc in self.contributions:
                p = new.p
                table.add(p)
                a = new.a(href=self.c.get_url('inbox_doc', id=doc.contribution)).add(doc.title)
                p.add(a)
                p.add(' (')
                a = new.a(href=self.c.get_url('edit', id=doc.contribution)).add('edit')
                p.add(a)
                p.add(') ')
        return self._center
        
