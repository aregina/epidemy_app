from datetime import datetime, timedelta

import requests
from push_notifications.models import APNSDevice, GCMDevice
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D

from epidemy_api.models import YupeConcerts, Fan


def city_coordinates(city_name):
    request_str = 'https://geocode-maps.yandex.ru/1.x/?format=json&geocode={}&results=1'.format(city_name)
    city_data = requests.get(request_str)
    city_point = city_data.json()['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']
    longitude, latitude = city_point['pos'].split()
    city_point = Point(float(longitude), float(latitude))
    return city_point


def send_push():
    one_day_ago = datetime.today() - timedelta(days=1)
    new_concerts = YupeConcerts.objects.using('epidemy_legacy').filter(creation_date__gte=one_day_ago)
    send_info_for_fan(new_concerts, 'Уже {} концерт группы "Эпидемия" в городе {}.')

    after_month_concert = YupeConcerts.objects.using('epidemy_legacy').filter(
        creation_date__lte=one_day_ago,
        date__gte=one_day_ago + timedelta(days=30),
        date__lte=one_day_ago + timedelta(days=31),
    )
    send_info_for_fan(after_month_concert, 'Уже через месяц, {} концерт группы "Эпидемия" в городе {}.')

    after_week_concert = YupeConcerts.objects.using('epidemy_legacy').filter(
        creation_date__lte=one_day_ago,
        date__gte=one_day_ago + timedelta(days=7),
        date__lte=one_day_ago + timedelta(days=8),
    )
    send_info_for_fan(after_week_concert, 'Уже через неделю, {} концерт группы "Эпидемия" в городе {}.')

    tomorrow = datetime.today().replace(hour=0, minute=0) + timedelta(days=1)
    after_day_concert = YupeConcerts.objects.using('epidemy_legacy').filter(
        creation_date__lte=one_day_ago,
        date__gte=tomorrow,
        date__lte=tomorrow + timedelta(days=1),
    )
    send_info_for_fan(after_day_concert, 'Уже завтра, {} концерт группы "Эпидемия" в городе {}.')


def send_info_for_fan(concerts, template):
    for concert in concerts:
        center_point = city_coordinates(concert.title)
        fans_for_notifications = Fan.objects.filter(fan_point__dwithin=(center_point, D(km=50)))
        for fan in fans_for_notifications:
            if fan.device_os_type == Fan.OS_TYPE.ios:
                device = APNSDevice(registration_id=fan.device_token)
            else:
                device = GCMDevice(registration_id=fan.device_token)
            concert_date = concert.date.strftime('%d.%m.%Y')
            message_for_notification = template.format(concert_date, concert.title)
            device.send_message(message_for_notification)