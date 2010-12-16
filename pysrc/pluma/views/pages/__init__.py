from slique.html.document import document
from django.utils.encoding import force_unicode


class Page(document):
    
    def __init__(self, context, title):
        super(Page, self).__init__()
        self.c = context
        
        # Add title
        self.head.title.add(force_unicode(title))
        
        # Add css to head
        
        # Add js to head

