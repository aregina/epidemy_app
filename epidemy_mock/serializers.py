from rest_framework import serializers
from .models import YupeConcerts, YupeNews, Fan


class ConcertsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = YupeConcerts
        fields = ('date', 'title', 'place', 'short_text', 'full_text')


class NewsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = YupeNews
        fields = ('date', 'title', 'short_text', 'full_text')


class FanSerializer(serializers.Serializer):
    OS_TYPE = (
        ('I', 'ios'),
        ('A', 'android')
    )
    device_token = serializers.CharField(max_length=255)
    device_os_type = serializers.CharField(max_length=1)
    fan_point = serializers.ListField()

    def validate(self, attrs):
        if len(attrs['fan_point']) != 2:
            raise serializers.ValidationError("fan_point expects 2 coordinates")
        return super(FanSerializer, self).validate(attrs)

    def create(self, validated_data):
        coordinates = validated_data['fan_point']
        points = 'POINT({} {})'.format(coordinates[0], coordinates[1])
        validated_data['fan_point'] = points
        return Fan.objects.create(**validated_data)

    class Meta:
        model = Fan
