from mongoengine import Document, StringField,  DateTimeField, ReferenceField, NULLIFY

from authentication.models import User

# Create your models here.
class Video_Upld(Document):
    title = StringField(max_length=500)
    description = StringField(max_length=5000)
    video_url = StringField()
    uploaded_by = ReferenceField(User, reverse_delete_rule=NULLIFY, related_name = "videos")
    uploaded_at = DateTimeField()