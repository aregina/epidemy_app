import datetime
from rest_framework import viewsets
from .models import YupeConcerts, YupeNews, Fan
from .serializers import ConcertsSerializer, NewsSerializer, FanSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from push_notifications.models import APNSDevice
from django.http import HttpResponse
import requests


class ConcertsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    one_day_ago = datetime.date.today() - datetime.timedelta(days=1)  # WRONG!
    queryset = YupeConcerts.objects.using('epidemy_legacy').filter(date__gte=one_day_ago).order_by('date')
    serializer_class = ConcertsSerializer


class NewsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = YupeNews.objects.using('epidemy_legacy').order_by('-date')
    serializer_class = NewsSerializer


class FanViewSet(viewsets.ModelViewSet):
    queryset = Fan.objects.all()
    serializer_class = FanSerializer


def current_datetime(request):
    print(312321312312312)
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    device = APNSDevice.objects.get(registration_id='8bab1b21edbba5b8a92acd3b33ce0c6d461919504b9d8be3e963a9561880d2ff')
    requests.packages.urllib3.disable_warnings()
    device.send_message("\u263A")
    return HttpResponse(html)


@api_view(['POST'])
def create_fan(request):
    serializer = FanSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

