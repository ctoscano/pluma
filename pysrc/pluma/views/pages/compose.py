'''
Created on Nov 24, 2010

@author: ctoscano
'''
from pluma.views.pages import Page
from pluma.views.language import ukgettext as _
from slique.html.html import new
from pluma.views import csrf_token

class Compose(Page):
    
    def __init__(self, context, contrib):
        self.contrib = contrib
        super(Compose, self).__init__(context, _('title_compose'))
        self.body.add(self._make_form())
        
    def _make_form(self):
        form = new.form(method="POST")
        
        form.add(csrf_token(self.c.request))
        form.add(new.input(type="text", name="title", value=self.contrib['title'] or 'title'))
        form.add(new.textarea(name="content", style="width:100%;height:300px").addHTML(self.contrib.rendered_content or 'content'))
        form.add(new.button(type='submit').add(_('submit_publish')))
        
        # only for new contributions
        #TODO: support some switching
        if '_id' not in self.contrib:
            select = new.select(name='type')
            for type in ('plain', 'html'):
                option = new.option(value=type).add(_('cont_type_name_%s' % type))
                if self.contrib.type == type: option.set(selected='true')
                select.add(option)
            form.add(select)
        
        return form
