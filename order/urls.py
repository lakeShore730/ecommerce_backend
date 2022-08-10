from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'orders', views.OrderViewSet, basename='orders')
router.register(f'order-items', views.OrderItemViewSet, basename='order_items')

urlpatterns = [
    path('', include(router.urls)),
]

