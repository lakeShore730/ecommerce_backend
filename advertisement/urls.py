from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'advertisement', views.AdvertisementViewSet, basename='advertisement')

urlpatterns = [
    path('', include(router.urls)),
]

