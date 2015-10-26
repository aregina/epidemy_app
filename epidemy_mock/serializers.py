from rest_framework import serializers
from .models import YupeConcerts, YupeNews


class ConcertsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = YupeConcerts


class NewsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = YupeNews
