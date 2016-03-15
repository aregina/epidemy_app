from datetime import date, timedelta

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import YupeConcerts, YupeNews, Fan
from .serializers import ConcertsSerializer, NewsSerializer, FanSerializer


class ConcertsViewSet(ModelViewSet):
    serializer_class = ConcertsSerializer

    def get_queryset(self):
        return YupeConcerts.objects.using('epidemy_legacy').filter(date__gte=date.today() - timedelta(days=1)).order_by('date')


class NewsViewSet(ModelViewSet):
    serializer_class = NewsSerializer
    queryset = YupeNews.objects.using('epidemy_legacy').order_by('-date')


class FanViewSet(ModelViewSet):
    serializer_class = FanSerializer
    queryset = Fan.objects.all()


@api_view(['POST'])
def create_fan(request):
    serializer = FanSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
