import re
import pymongo
import markdown
from datetime import datetime, date, timedelta
from bson import ObjectId

from mongoengine import *
from mongoengine.django.auth import User as Auth_User
from mongoengine.connection import _get_db


class User(Auth_User):
    
    def get_inbox(self):
        return GeneralEnvelope.objects.filter(recipient=self).order_by('-updated_date')


class Contribution(Document):
    # Basic information
    title = StringField(required=True)
    author = ReferenceField(User)
    creation_date = DateTimeField(required=True, default=datetime.now)
    updated_date = DateTimeField(required=True, default=datetime.now)
    domain = StringField(required=False, db_field='D')
    uri = StringField(required=False, db_field='U')
    mode = StringField(db_field='m')
    
    # Access information
    is_public = BooleanField(default=False)
    accessors = ListField(ReferenceField(User))
    
    # Content
    rendered_content = StringField(required=True, default='')
    
    content_type = StringField(db_field='ct', default='text/plain')
    
    def __init__(self, **values):
        self._new_accessors = []
        super(Contribution, self).__init__(**values)
        
    @classmethod
    def factory(cls, id=None, type=None, domain=None, uri=None):
        if id is None and type is None and (domain is None and uri is None):
            return None
        
        if id or (domain and uri):
            query = {'_id': ObjectId(id)}
            if domain: 
                query['D'] = domain
            if domain and uri:
                query['U'] = uri
                del query['_id']
            
            values = _get_db().contribution.find_one(query)
            
            if values is None:
                return None
            values.setdefault('type')
            type = values['type']
        elif type:
            values = {}
        
        
        if type == 'html':
            return HtmlContribution._from_son(values)
        elif type == 'markdown':
            return MarkdownContribution._from_son(values)
        else:
            return Contribution._from_son(values)
        
    @classmethod
    def get_all(cls):
        return cls.objects.all()
    
    def save(self):
        super(Contribution, self).save(True)
        already_touched = []
        for acc in self._new_accessors:
            envelope = Envelope.create(self, acc)
            envelope.save()
            already_touched.append(acc)
        for acc in self.accessors:
            if acc in already_touched: continue
            GeneralEnvelope.touch(self)
            
    def add_accessor(self, accessor):
        self._new_accessors.append(accessor)
        if accessor not in self.accessors:
            self.accessors.append(accessor)
            return True
        return False
    
    def is_accessible(self, user):
        return self.is_public or user in self.accessors
    
    def get_text(self):
        '''must return a string'''
        return self.rendered_content
    
    def set_text(self, text):
        self.rendered_content = text
    
    def get_draft_text(self, user):
        if not hasattr(self, '_id'):                # new contribution; no draft
            return self.get_text()       
        else: 
            draft = Draft.get_draft(user, self._id)
            return draft.content if draft else self.get_text() 
    
    def set_url(self, domain, uri):
        #TODO: better input validation
        if domain not in (False, None, '', 'Domain') and uri not in ('URI', False):
            self.domain = domain
            self.uri = uri
            return True
        else:
            return False
        
    def set_mode(self, mode):
        self.mode = mode
        if mode == 'css':
            self.content_type = 'text/css'
        elif mode == 'javascript':
            self.content_type = 'text/javascript'
            

class HtmlContribution(Contribution):
    content_type = StringField(db_field='ct', default='text/html')
    
class MarkdownContribution(Contribution):
    raw_content = StringField(required=True, default='')
    content_type = StringField(db_field='ct', default='text/html')
    
    def get_text(self):
        return self.raw_content
        
    def set_text(self, text):
        self.raw_content = text
        self.rendered_content = markdown.markdown(text, ['codehilite', 'extra', 'toc'], 'escape')

class Draft(Document):
    author = StringField(required=True, db_field='a')
    contribution = StringField(db_field='c')
    title = StringField(required=True, db_field='t') # used for drafts tab
    content = StringField(db_field='txt', default='')
    
    meta = {
        'allow_inheritance': False,
    }
    
    @classmethod
    def get_user_drafts(cls, user):
        drafts = []
        if hasattr(user, '_id') and user._id != '':
            drafts =  Draft.objects.filter(author=str(user._id))
        return drafts
    
    def set_user(self, user):
        self.author = unicode(user._id)
        
    def set_contribution(self, contrib):
        self.contrib = contrib._id
        
    @classmethod
    def get_draft(cls, user, contrib_id):
        '''returns target object or None'''
        draft =  Draft.objects.filter(author=str(user._id), 
                                contribution=str(contrib_id)).first()
        return draft
    
    @classmethod
    def with_id(cls, user, draft_id):
        return cls.objects.filter(author=str(user._id)).with_id(draft_id)
    
    @classmethod
    def save_draft(cls, user, contrib):
        ''' @param user: required
            @param contrib: ignoring id if blank; always use text
        '''
        main_vars = {'a':unicode(user._id)}
        
        # Only set contribution ID if ID not blank
        if hasattr(contrib, '_id') and contrib._id != '': 
            main_vars['c'] = unicode(contrib._id)
        
        _get_db().draft.update(main_vars, 
                               {'$set':{'txt':contrib.get_text(),
                                        't':contrib.title}}, 
                               upsert=True)
        
    @classmethod
    def remove(cls, user=False, contrib=False, draft=False):
        if hasattr(contrib, '_id'):
            _get_db().draft.remove({'a':unicode(user._id),
                                    'c':unicode(contrib._id)})
        elif hasattr(draft, '_id'):
            _get_db().draft.remove({'a':unicode(user._id),
                                    '_id':ObjectId(draft._id)})
        

class Envelope(Document):
    '''Corresponds to a row in the user's mail box.
    '''
    title = StringField(required=True)
    author = ReferenceField(User)
    contribution = StringField(required=True) # faster than reference field
    created_date = DateTimeField(required=True, default=datetime.now)
    updated_date = DateTimeField(required=True, default=datetime.now)
    
    @classmethod
    def create(cls, contribution, accessor):
        if True: # general account
            envelope = GeneralEnvelope()
            envelope.title = contribution.title
            envelope.author = contribution.author
            envelope.contribution = unicode(contribution[contribution._meta['id_field']])
            envelope.recipient = accessor
            return envelope
        elif False: # group access
            pass
        elif False: # premium account
            pass
    
class PremiumEnvelope(Envelope):
    pass

class GeneralEnvelope(Envelope):
    '''Envelope used in the standard mailbox.
    '''
    recipient = ReferenceField(User)
    
    @classmethod
    def touch(cls, contrib):
        '''updates all envelopes with new modification date
        '''
        _get_db().envelope.update({'contribution':unicode(contrib[contrib._meta['id_field']])}, 
                                  {'$set':{'updated_date':datetime.now(), 'title':contrib.title}})
    
class PublicEnvelope(Envelope):
    '''Placed in the public inbox; used for public access.
    '''
    pass

