from datetime import datetime
from bs4 import BeautifulSoup
from rest_framework.serializers import (
    HyperlinkedModelSerializer, SerializerMethodField, Serializer, CharField, ListField, ValidationError
)
from .models import YupeConcerts, YupeNews, Fan


def processing_text(document):
    if document.find("iframe") != -1 and document.find("</iframe>") == -1:
        document = document.replace("/iframe", "></iframe>").replace("iframe src", "<iframe src")

    soup = BeautifulSoup(document, 'html.parser')
    imgs = []
    videos = []

    for video in soup.find_all("iframe"):
        youtube_url = video.extract().get("src")
        if youtube_url.startswith("//"):
            youtube_url = youtube_url.replace("//", "")
        videos.append(youtube_url)

    for img in soup.find_all("img"):
        img_content = img.extract()
        soup.contents += img_content.renderContents()
        url = img_content.get("src")
        if url:
            if url.find("http://") == -1:
                url = "http://epidemia.ru" + url
            imgs.append(url)

    return str(soup), imgs, videos


def delete_images_and_videos(document):
    return processing_text(document)[0]


def selection_images(document):
    return processing_text(document)[1]


def selection_videos(document):
    return processing_text(document)[2]


class ContentSerializer(HyperlinkedModelSerializer):
    pass


class ConcertsSerializer(HyperlinkedModelSerializer):
    image_urls = SerializerMethodField()

    @staticmethod
    def get_image_urls(obj):
        return ["http://epidemia.ru/uploads/concerts/{}.big.jpg".format(obj.id)]

    class Meta:
        model = YupeConcerts
        fields = ('date', 'title', 'place', 'short_text', 'full_text', 'image_urls')


class NewsSerializer(HyperlinkedModelSerializer):
    image_urls = SerializerMethodField()
    video_urls = SerializerMethodField()
    full_text = SerializerMethodField()
    short_text = SerializerMethodField()
    date = SerializerMethodField()

    @staticmethod
    def get_date(obj):
        return datetime(*(obj.date.timetuple()[:6]))

    @staticmethod
    def get_image_urls(obj):
        return selection_images(obj.full_text)

    @staticmethod
    def get_video_urls(obj):
        return selection_videos(obj.full_text)

    @staticmethod
    def get_full_text(obj):
        return delete_images_and_videos(obj.full_text)

    @staticmethod
    def get_short_text(obj):
        return delete_images_and_videos(obj.short_text)

    class Meta:
        model = YupeNews
        fields = ('date', 'title', 'short_text', 'full_text', 'image_urls', 'video_urls')


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
            raise ValidationError("fan_point expects 2 coordinates")
        return super(FanSerializer, self).validate(attrs)

    def create(self, validated_data):
        coordinates = validated_data['fan_point']
        points = 'POINT({} {})'.format(coordinates[0], coordinates[1])
        validated_data['fan_point'] = points
        return Fan.objects.create(**validated_data)

    class Meta:
        model = Fan
