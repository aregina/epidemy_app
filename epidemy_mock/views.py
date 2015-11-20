import datetime

from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from push_notifications.models import APNSDevice
import requests

from django.contrib.gis.geos import Point

from .models import YupeConcerts, YupeNews, Fan
from .serializers import ConcertsSerializer, NewsSerializer, FanSerializer


class ConcertsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    serializer_class = ConcertsSerializer

    def get_queryset(self):
        return YupeConcerts.objects.using('epidemy_legacy').filter(
            date__gte=datetime.date.today() - datetime.timedelta(days=1)).order_by('date')


class NewsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = YupeNews.objects.using('epidemy_legacy').order_by('-date')
    serializer_class = NewsSerializer


class FanViewSet(viewsets.ModelViewSet):
    queryset = Fan.objects.all()
    serializer_class = FanSerializer


def city_coordinates(city_name):
    request_str = 'https://geocode-maps.yandex.ru/1.x/?format=json&geocode={}&results=1'.format(city_name)
    city_data = requests.get(request_str)
    city_point = city_data.json()['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']
    longitude, latitude = city_point['pos'].split()
    city_point = Point(float(longitude), float(latitude))
    return city_point


def send_push(request):
    one_day_ago = datetime.datetime.today() - datetime.timedelta(days=1)
    new_concerts = YupeConcerts.objects.using('epidemy_legacy').filter(creation_date__gte=one_day_ago)
    for concert in new_concerts:
        center_point = city_coordinates(concert.title)
        fans_for_notifications = Fan.objects.filter(fan_point__dwithin=(center_point, 1.4))
        for fan in fans_for_notifications:
            device = APNSDevice(registration_id=fan.device_token)
            concert_date = concert.date.strftime('%d.%m.%Y')
            message_for_notification = 'Уже {} концерт группы "Эпидемия" в городе {}.'.format(concert_date,
                                                                                              concert.title)
            device.send_message(message_for_notification)


@api_view(['POST'])
def create_fan(request):
    serializer = FanSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
