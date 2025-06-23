from django.db import models
from mongoengine import Document, StringField, DateTimeField
# Create your models here.

class User(Document):
    name = StringField(max_length=100)
    email = StringField(max_length=200, unique=True)
    password = StringField(max_length=500)
    created_at = DateTimeField(auto_now_add= True)
    
    meta = {'collection': 'users'}