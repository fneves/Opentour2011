from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4
import datetime

class Post(models.Model):
    uuid = models.CharField('identifier', max_length=36, unique=True)
    text = models.TextField('Message',max_length=200, blank=False)
    pub_date = models.DateTimeField('date published')
    publisher = models.ForeignKey(User)

    def __unicode__(self):
        return self.uuid
 
    def save(self):
        if not self.uuid:
            self.uuid = str(uuid4())  # random so it can't be easily guessed
            self.pub_date = datetime.datetime.now()
        super(Post, self).save()

    def likes(self):
        return self.likes_set.filter(description='like')
    
    def dislikes(self):
        return self.likes_set.filter(description='dislike')

class Comment(models.Model):
    text = models.TextField(max_length=200, blank=False)
    pub_date = models.DateTimeField('date published')
    comentator = models.ForeignKey(User)
    in_response_to = models.ForeignKey(Post)

class Likes(models.Model):
    post = models.ForeignKey(Post)
    description = models.CharField(max_length=10)
    liker = models.ForeignKey(User)
