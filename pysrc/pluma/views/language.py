'''
Created on Nov 24, 2010

@author: ctoscano
'''

from django.utils.translation import ugettext

def ukgettext(unicode, IS_SHORT=False):
    '''use a key to translate a string'''
    if IS_SHORT:
        return ugettext(unicode)
    else:
        return ugettext(default_dictionary[unicode])

default_dictionary = {
'title_home':'plu.ma - write for yourself, your friends, and your fans',
'title_compose':'compose - plu.ma',
'submit_publish':'Publish!',
'submit_save':'Save',
'discard':'Discard',
'edit':'Edit',
'is_public':'Make publicly available.',
'domain':'Domain',
'uri':'URI',
'Sign Up':'Sign Up',
'Sign In':'Sign In',

'title_drafts':'Drafts',


'cont_type_name_plain':'Plain Text',
'cont_type_name_html':'HTML',
'cont_type_name_css':'CSS',
'cont_type_name_javascript':'JavaScript',
'cont_type_name_markdown':'Markdown',
}
