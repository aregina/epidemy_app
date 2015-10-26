from django.db import models
from django.utils import timezone


class YupeConcerts(models.Model):
    category_id = models.IntegerField(blank=True, null=True)
    lang = models.CharField(max_length=2, blank=True, null=True)
    creation_date = models.DateTimeField()
    change_date = models.DateTimeField()
    date = models.DateTimeField()
    year = models.IntegerField()
    title = models.CharField(max_length=150)
    place = models.CharField(max_length=255)
    alias = models.CharField(max_length=150)
    short_text = models.TextField(blank=True, null=True)
    full_text = models.TextField()
    image = models.CharField(max_length=300, blank=True, null=True)
    link = models.CharField(max_length=300, blank=True, null=True)
    user_id = models.IntegerField()
    status = models.IntegerField()
    is_protected = models.IntegerField()
    keywords = models.CharField(max_length=150)
    description = models.CharField(max_length=250)

    class Meta:
        managed = False
        db_table = 'yupe_concerts'
        unique_together = (('alias', 'lang'),)


class YupeNews(models.Model):
    category_id = models.IntegerField(blank=True, null=True)
    lang = models.CharField(max_length=2, blank=True, null=True)
    creation_date = models.DateTimeField()
    change_date = models.DateTimeField()
    date = models.DateField()
    title = models.CharField(max_length=150)
    alias = models.CharField(max_length=150)
    short_text = models.TextField(blank=True, null=True)
    full_text = models.TextField()
    image = models.CharField(max_length=300, blank=True, null=True)
    link = models.CharField(max_length=300, blank=True, null=True)
    user_id = models.IntegerField()
    status = models.IntegerField()
    is_protected = models.IntegerField()
    keywords = models.CharField(max_length=150)
    description = models.CharField(max_length=250)

    class Meta:
        managed = False
        db_table = 'yupe_news'
        unique_together = (('alias', 'lang'),)
