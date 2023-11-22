from django.db import models
from django.contrib.auth.models import User
from Shows.models import Event
# Create your models here.


class ChordSheet(models.Model):
    title = models.TextField("Song Title",max_length=50)
    initial_key = models.PositiveSmallIntegerField(null=True)
    initial_tempo = models.PositiveSmallIntegerField(null=True)
    initial_metre_1 = models.PositiveSmallIntegerField(default=4)
    initial_metre_2 = models.PositiveSmallIntegerField(default=4)
    content = models.JSONField(default=list)
    def getFinalKey(self):
        key = self.initial_key
        items: list[dict] = self.content
        for item in items:
            if 'transpose' in item:
                key += item['transpose']
        while key < 0:
            key += 12
        while key >= 12:
            key -= 12
        return key

class ChordSheetRoles(models.Model):
    sheet = models.ForeignKey(ChordSheet,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    role = models.PositiveSmallIntegerField()
    lastupdate = models.DateTimeField(auto_now=True)

class EventItemOrder(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='items')
    nr = models.PositiveSmallIntegerField()
    sheet = models.ForeignKey(ChordSheet, on_delete=models.CASCADE,null=True)
    proposed_duration = models.DurationField(null=True)

    class Meta:
        unique_together = [('event', 'nr')]
        ordering = ['event', 'nr']

