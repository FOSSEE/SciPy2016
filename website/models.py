from django.db import models
from django.contrib.auth.models import User

from social.apps.django_app.default.models import UserSocialAuth
from scipy2016 import settings

def get_document_dir(instance, filename):
    ename, eext = instance.user.email.split("@")
    fname, fext = filename.split(".")
    return '%s/attachment/%s.%s' % (instance.user, str(instance.user)+str(fext), fext)

class Proposal(models.Model):
    user = models.ForeignKey(User)
    about_me = models.TextField(max_length=500)
    email = models.CharField(max_length=128)
    phone = models.CharField(max_length = 20)
    title = models.CharField(max_length=250)
    abstract = models.TextField(max_length=700)
    prerequisite = models.CharField(max_length=250)
    attachment = models.FileField(upload_to=get_document_dir)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    
class Comments(models.Model):
    proposal = models.ForeignKey(Proposal)
    user = models.ForeignKey(User)
    comment = models.CharField(max_length=700)
