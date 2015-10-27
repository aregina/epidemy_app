from rest_framework import serializers
from .models import YupeConcerts, YupeNews


class ConcertsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = YupeConcerts
        fields = ('date', 'title', 'place', 'short_text', 'full_text')



class NewsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = YupeNews
        fields = ('date', 'title', 'short_text', 'full_text')
