'''
Created on Nov 24, 2010

@author: ctoscano
'''
from pluma.views.pages import WorkPage
from pluma.views.language import ukgettext as _
from slique.html.html import new
from pluma.views import csrf_token

class Compose(WorkPage):
    
    def __init__(self, context, contrib):
        self.contrib = contrib
        super(Compose, self).__init__(context, _('title_compose'))
        self.center.add(self._make_form())
        
        self.head.addHTML('''
        <script src="/js/jquery-1.5.1.min.js" type="text/javascript" charset="utf-8"></script>
        <script src="/js/ace/ace.js" type="text/javascript" charset="utf-8"></script>
        <script src="/js/ace/mode-html.js" type="text/javascript" charset="utf-8"></script>
        <script src="/js/ace/theme-eclipse.js" type="text/javascript" charset="utf-8"></script>
        <script src="/js/pluma.js" type="text/javascript" charset="utf-8"></script>
        <script>
            window.onload = function () {
                window.p = new Pluma({ace:true});
                p.init();
                p.initComposer('composer', 'basic_composer', 'composer_form');
                p.setEditorMode('%(mode)s');
            }
        </script>
        ''' % {'mode' : self.contrib.mode or 'plain'})
        
    def _make_form(self):
        form = new.form(id="composer_form", method="POST")
        
        form.add(csrf_token(self.c.request))
        form.add(new.input(type="text", name="title", value=self.contrib['title'] or 'title'))
        form.add(new.div(id="composer"))
        form.add(new.textarea(id="basic_composer", name="content", style="height:400px;position:relative;").
                 add(self.contrib.get_draft_text(self.c.user) or 'content'))
        form.add(new.button(type='submit').add(_('submit_publish')))
        form.add(new.input(type='submit', value=_('submit_save'), name="save"))
        form.add(new.input(type='submit', value=_('discard'), name="discard"))
        
        # Optional
        form.add(new.input(type='text', value=self.contrib.domain or _('domain'), name="domain"))
        # Optional
        form.add(new.input(type='text', value=self.contrib.uri or _('uri'), name="uri"))
        # Optional
        is_public = new.input(id='is_public', type='checkbox', value='true', 
                           name="is_public")
        if self.contrib['is_public']: is_public.set(checked='checked')
        form.add(is_public)
        form.add(new.label(fr='is_public').add(_('is_public')))
        
        # only for new contributions
        #TODO: support some switching
        if '_id' not in self.contrib:
            select = new.select(id="type_select",name='type')
            for type in ('plain', 'html', 'css', 'javascript', 'markdown'):
                option = new.option(value=type).add(_('cont_type_name_%s' % type))
                select.add(option)
            form.add(select)
        
        return form
