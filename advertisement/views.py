from rest_framework import viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import AdvertisementSerializer
from .models import Advertisement

class AdvertisementViewSet(viewsets.ViewSet):
   
    def list(self, request):
        queryset = Advertisement.objects.filter(is_active=True)
        serializer = AdvertisementSerializer(queryset, many=True, context={"request":request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Advertisement.objects.filter(is_active=True)
        advertisement = get_object_or_404(queryset, pk=pk)
        serializer = AdvertisementSerializer(advertisement, context={"request":request})
        return Response(serializer.data)


 
