from django.db import models
from django.utils import timezone


# Create your models here.
class Event(models.Model):
    id = models.AutoField(primary_key=True)
    poster_url = models. URLField()
    text = models.TextField()
    date = models.DateTimeField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, default='')
    title = models.CharField(max_length=100, blank=True, default='')
    place = models.CharField(max_length=100, blank=True, default='')

