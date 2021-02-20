from django.db.models import *
from django.contrib.gis.db.models import PointField
from django.contrib.gis.db.models import GeoManager
from django.utils import timezone


class YupeConcerts(Model):
    category_id = IntegerField(blank=True, null=True)
    lang = CharField(max_length=2, blank=True, null=True)
    creation_date = DateTimeField()
    change_date = DateTimeField()
    date = DateTimeField()
    year = IntegerField()
    title = CharField(max_length=150)
    place = CharField(max_length=255)
    alias = CharField(max_length=150)
    short_text = TextField(blank=True, null=True)
    full_text = TextField()
    image = CharField(max_length=300, blank=True, null=True)
    link = CharField(max_length=300, blank=True, null=True)
    user_id = IntegerField()
    status = IntegerField()
    is_protected = IntegerField()
    keywords = CharField(max_length=150)
    description = CharField(max_length=250)

    class Meta:
        managed = False
        db_table = 'yupe_concerts'
        unique_together = (('alias', 'lang'),)


class YupeNews(Model):
    category_id = IntegerField(blank=True, null=True)
    lang = CharField(max_length=2, blank=True, null=True)
    creation_date = DateTimeField()
    change_date = DateTimeField()
    date = DateField()
    title = CharField(max_length=150)
    alias = CharField(max_length=150)
    short_text = TextField(blank=True, null=True)
    full_text = TextField()
    image = CharField(max_length=300, blank=True, null=True)
    link = CharField(max_length=300, blank=True, null=True)
    user_id = IntegerField()
    status = IntegerField()
    is_protected = IntegerField()
    keywords = CharField(max_length=150)
    description = CharField(max_length=250)

    class Meta:
        managed = False
        db_table = 'yupe_news'
        unique_together = (('alias', 'lang'),)


class Fan(Model):
    OS_TYPE = (
        ('I', 'ios'),
        ('A', 'android')
    )
    fan_point = PointField()
    device_token = CharField(max_length=255, unique=True)
    device_os_type = CharField(max_length=1, choices=OS_TYPE)
    objects = GeoManager()
