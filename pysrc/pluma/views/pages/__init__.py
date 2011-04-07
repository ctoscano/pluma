from slique.html.document import document
from slique.html.html import new
from django.utils.encoding import force_unicode
from slique.html.table import VerticalTable


class Page(document):
    
    def __init__(self, context, title):
        self._top = None
        self._left = None
        
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
