import datetime

from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import YupeConcerts, YupeNews, Fan
from .serializers import ConcertsSerializer, NewsSerializer, FanSerializer
from backgraund_worker import send_push


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


@api_view(['POST'])
def create_fan(request):
    serializer = FanSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
