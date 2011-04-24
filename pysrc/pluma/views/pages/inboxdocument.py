'''
Created on Nov 24, 2010

@author: ctoscano
'''
from slique.html.html import new
from pluma.views.pages import WorkPage
from pluma.views.language import ukgettext as _

class InboxDocument(WorkPage):
    
    def __init__(self, context, contribution_id):
        self.contribution_id = contribution_id
        super(InboxDocument, self).__init__(context, '')
        self.init()

    @property
    def center(self):
        if self._center is None:
            super(InboxDocument, self).center
            div = new.div
            self._center.add(div)
            
            iframe = new.iframe(src=self.c.get_url('doc', id=self.contribution_id),
                               id='inbox_doc',
                               cls='inbox_doc', 
                               frameborder=0, marginwidth=0, marginheight=0)
            div.add(iframe)
        return self._center

    def init(self):
        self.head.addHTML('''
        <script src="/js/pluma.js" type="text/javascript" charset="utf-8"></script>
        <script>
            window.onload = function () {
                window.p = new Pluma();
                p.init();
                p.resizeInboxDoc("%(iframe_id)s");
            }
        </script>
        ''' % {'iframe_id' : 'inbox_doc'})
        self.top.insert(0, new.a(href=self.c.get_url('edit', id=self.contribution_id)).add(_('edit')))
