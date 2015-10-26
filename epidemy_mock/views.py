from rest_framework import viewsets
from .models import YupeConcerts, YupeNews
from .serializers import ConcertsSerializer, NewsSerializer
import datetime


class ConcertsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    two_days_ago = datetime.date.today() - datetime.timedelta(days=1)
    queryset = YupeConcerts.objects.filter(date__gte=two_days_ago).order_by('date')
    serializer_class = ConcertsSerializer


class NewsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = YupeNews.objects.order_by('-date')
    serializer_class = NewsSerializer
