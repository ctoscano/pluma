'''
Created on Nov 24, 2010

@author: ctoscano
'''
from pluma.views.pages import WorkPage
from pluma.views.language import ukgettext as _
from slique.html.html import new
from slique.html.table import VerticalTable

class Drafts(WorkPage):
    
    def __init__(self, context, contributions):
        self.contributions = contributions
        super(Drafts, self).__init__(context, _('title_drafts'))

        table = VerticalTable()
        self.center.add(table)
        
        for doc in self.contributions:
            p = new.p
            table.add(p)
            if hasattr(doc, 'contribution') and doc.contribution:
                url = self.c.get_url('edit', id=doc.contribution)
            else:
                url = self.c.get_url('draft', id=doc._id)
            a = new.a(href=url).add(doc.title)
            p.add(a)
        