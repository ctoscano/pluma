from slique.html.document import document
from slique.html.html import new
from django.utils.encoding import force_unicode
from slique.html.table import VerticalTable


class Page(document):
    
    def __init__(self, context, title):
        self._top = None
        self._left = None
        self._center = None
        
        super(Page, self).__init__()
        self.c = context
        
        # Add title
        self.head.title.add(force_unicode(title))
        
        # Add css to head
        self.head.add(new.link(rel='stylesheet',type='text/css', href='/css/reset.css'))
        self.head.add(new.link(rel='stylesheet',type='text/css', href='/css/pluma.css'))
        
        # Add js to head
        
        self.body.add(self.top)
        self.body.add(self.left)
        self.body.add(self.center)

    @property
    def top(self):
        if self._top is None: 
            self._top = new.div(cls='top')
            
            if self.c.user.is_authenticated():
                self._top.add(new.a(href=self.c.get_url('signout')
                            ).add('Sign Out'))
        return self._top

    @property
    def left(self):
        if self._left is None:
            self._left = new.div(cls='lc')
            
        return self._left
    
    @property
    def center(self):
        if self._center is None:
            self._center = new.div(cls='cc')
            
        return self._center
    
class WorkPage(Page):
    
    def __init__(self, context, title):
        super(WorkPage, self).__init__(context, title)
        
    @property
    def left(self):
        if self._left is None:
            super(WorkPage, self).left
            
            table = VerticalTable()
            self._left.add(table)
            table.add(new.a(href=self.c.get_url('inbox')
                                ).add('Inbox'))
            table.add(new.a(href=self.c.get_url('compose')
                            ).add('compose'))
            table.add(new.a(href=self.c.get_url('drafts')
                            ).add('drafts'))
        return self._left
    
