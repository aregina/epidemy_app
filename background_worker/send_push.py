import datetime

import requests
from push_notifications.models import APNSDevice
from django.contrib.gis.geos import Point

from epidemy_api.models import YupeConcerts, Fan


def city_coordinates(city_name):
    request_str = 'https://geocode-maps.yandex.ru/1.x/?format=json&geocode={}&results=1'.format(city_name)
    city_data = requests.get(request_str)
    city_point = city_data.json()['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']
    longitude, latitude = city_point['pos'].split()
    city_point = Point(float(longitude), float(latitude))
    return city_point


def send_push():
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
