import re
import pymongo
import markdown
from datetime import datetime, date, timedelta

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
    
    # Access information
    is_public = BooleanField(default=False)
    accessors = ListField(ReferenceField(User))
    
    # Content
    rendered_content = StringField(required=True)
    
    content_type = 'text/plain'
    
    def __init__(self, **values):
        self._new_accessors = []
        super(Contribution, self).__init__(**values)
        
    @classmethod
    def factory(cls, id=None, type=None, domain=None, uri=None):
        if id is None and type is None and (domain is None and uri is None):
            return None
        
        if id or (domain and uri):
            query = {'_id': pymongo.objectid.ObjectId(id)}
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
    
    def get_text(self):
        return self.rendered_content
    
    def set_text(self, text):
        self.rendered_content = text
    
    def get_draft_text(self, user):
        if not hasattr(self, '_id'): return ''         # new contribution; no content
        
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

class HtmlContribution(Contribution):
    content_type = 'text/html'
    
class MarkdownContribution(Contribution):
    raw_content = StringField(required=True)
    content_type = 'text/html'
    
    def get_text(self):
        return self.raw_content
        
    def set_text(self, text):
        self.raw_content = text
        self.rendered_content = markdown.markdown(text, ['codehilite', 'extra', 'toc'], 'escape')

class Draft(Document):
    author = StringField(required=True, db_field='a')
    contribution = StringField(required=True, db_field='c')
    content = StringField()
    
    meta = {
        'allow_inheritance': False,
    }
    
    def set_user(self, user):
        self.author = user._id
        
    def set_contribution(self, contrib):
        self.contrib = contrib._id
        
    @classmethod
    def get_draft(cls, user, contrib_id):
        '''returns target object or None'''
        draft =  Draft.objects.filter(author=str(user._id), 
                                contribution=str(contrib_id)).first()
        return draft
    
    @classmethod
    def save_draft(cls, user, contrib):
        _get_db().draft.update({'a':unicode(user._id),
                                'c':unicode(contrib._id)}, 
                               {'$set':{'content':contrib.get_text()}}, 
                               upsert=True)
        
    @classmethod
    def remove(cls, user, contrib):
        if hasattr(contrib, '_id'):
            _get_db().draft.remove({'a':unicode(user._id),
                                    'c':unicode(contrib._id)})
        

class Envelope(Document):
    '''Corresponds to a row in the user's mail box.
    '''
    title = StringField(required=True)
    author = ReferenceField(User)
    contribution = StringField(required=True) # faster than reference field
    created = DateTimeField(required=True, default=datetime.now)
    updated = DateTimeField(required=True, default=datetime.now)
    
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
    '''Evenlope used in the standard mailbox.
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

