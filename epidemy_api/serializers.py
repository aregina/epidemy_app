from datetime import datetime, timezone
from collections import namedtuple

from bs4 import BeautifulSoup

from rest_framework.serializers import (
    HyperlinkedModelSerializer, SerializerMethodField, Serializer, CharField, ListField, ValidationError
)
from .models import YupeConcerts, YupeNews, Fan


class ConcertsSerializer(HyperlinkedModelSerializer):
    image_urls = SerializerMethodField()

    @staticmethod
    def get_image_urls(obj):
        return ['http://epidemia.ru/uploads/concerts/{}.big.jpg'.format(obj.id)]

    class Meta:
        model = YupeConcerts
        fields = ('date', 'title', 'place', 'short_text', 'full_text', 'image_urls')


class NewsSerializer(HyperlinkedModelSerializer):
    image_urls = SerializerMethodField()
    video_urls = SerializerMethodField()
    full_text = SerializerMethodField()
    short_text = SerializerMethodField()
    date = SerializerMethodField()

    class Meta:
        model = YupeNews
        fields = ('date', 'title', 'short_text', 'full_text', 'image_urls', 'video_urls')

    @staticmethod
    def process_text(document):
        if document.find('iframe') != -1 and document.find('</iframe>') == -1:
            document = document.replace('/iframe', '></iframe>').replace('iframe src', '<iframe src')

        soup = BeautifulSoup(document, 'html.parser')
        images = []
        videos = []

        for video in soup.find_all('iframe'):
            youtube_url = video.extract().get('src')
            if youtube_url.startswith('//'):
                youtube_url = youtube_url.replace('//', '')
            videos.append(youtube_url)

        for img in soup.find_all('img'):
            img_content = img.extract()
            soup.contents += img_content.renderContents()
            url = img_content.get('src')
            if url:
                if url.startswith('http') == -1:
                    url = 'http://epidemia.ru' + url
                images.append(url)

        Content = namedtuple('Content', ['text', 'images', 'videos'])
        return Content(str(soup), images, videos)

    @classmethod
    def delete_images_and_videos(cls, document):
        return cls.process_text(document).text

    @classmethod
    def select_images(cls, document):
        return cls.process_text(document).images

    @classmethod
    def select_videos(cls, document):
        return cls.process_text(document).videos

    @classmethod
    def get_image_urls(cls, obj):
        return cls.select_images(obj.full_text)

    @classmethod
    def get_video_urls(cls, obj):
        return cls.select_videos(obj.full_text)

    @classmethod
    def get_full_text(cls, obj):
        return cls.delete_images_and_videos(obj.full_text)

    @classmethod
    def get_short_text(cls, obj):
        return cls.delete_images_and_videos(obj.short_text)

    @staticmethod
    def get_date(obj):
        return datetime(*(obj.date.timetuple()[:6])).replace(tzinfo=timezone.utc)


class FanSerializer(Serializer):
    OS_TYPE = (
        ('I', 'ios'),
        ('A', 'android')
    )
    device_token = CharField(max_length=255)
    device_os_type = CharField(max_length=1)
    fan_point = ListField()

    def validate(self, attrs):
        if len(attrs['fan_point']) != 2:
            raise ValidationError('fan_point expects 2 coordinates')
        return super(FanSerializer, self).validate(attrs)

    def create(self, validated_data):
        log, lat = validated_data['fan_point']
        points = 'POINT({} {})'.format(log, lat)
        validated_data['fan_point'] = points
        return Fan.objects.create(**validated_data)

    class Meta:
        model = Fan
