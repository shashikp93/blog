from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(User,null=True)
    title = models.CharField(max_length=100)
    image = models.FileField(null=True,blank=True)
    content = models.TextField()
    updated = models.DateTimeField(auto_now=True,auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False,auto_now_add=True)

    def __unicode__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('detail',kwargs={"id":self.id})
        #return "/post_detail/%s/"%(self.id)

    class Meta:
        ordering=['-timestamp','-updated']
