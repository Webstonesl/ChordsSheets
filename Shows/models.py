from django.db import models
from django.contrib.auth.models import User, Group
from datetime import datetime, timedelta
# Create your models here.
class Event(models.Model):
    start = models.DateTimeField()
    title = models.TextField(max_length=100)
    def location(self):
        if (self.pk == None):
            return '/shows/new'
        else:
            return f'/shows/{self.pk}'
    def format_start(self):
        if(self.start != None):

            return self.start.__add__(timedelta(hours=2)).strftime('%Y-%m-%dT%H:%M:%S')
        else:
            return ''
class EventRole(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='EventRoles')
    event = models.ForeignKey(Event,on_delete=models.CASCADE)
    role = models.PositiveSmallIntegerField()


    