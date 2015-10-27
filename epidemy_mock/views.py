import datetime
from rest_framework import viewsets
from .models import YupeConcerts, YupeNews
from .serializers import ConcertsSerializer, NewsSerializer


class ConcertsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    one_day_ago = datetime.date.today() - datetime.timedelta(days=1)
    queryset = YupeConcerts.objects.filter(date__gte=one_day_ago).order_by('date')
    serializer_class = ConcertsSerializer


class NewsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = YupeNews.objects.order_by('-date')
    serializer_class = NewsSerializer
