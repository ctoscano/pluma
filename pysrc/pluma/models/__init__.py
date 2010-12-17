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
    def factory(cls, id=None, type=None):
        if id is None and type is None:
            return None
        
        if id:
            values = _get_db().contribution.find_one({'_id': pymongo.objectid.ObjectId(id)})
            
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


