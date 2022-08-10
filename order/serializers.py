from rest_framework import serializers
from .models import Order, Item
from product.models import Product
from django.shortcuts import get_object_or_404

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
    

class ItemSerializerForOrder(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['product', 'quantity']


class OrderCreationSerializer(serializers.ModelSerializer):
    items = ItemSerializerForOrder(many=True)
    class Meta:
        model = Order
        fields = ['remarks', 'items']


class OrderListSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True)
    class Meta: 
        model = Order
        fields = '__all__'
       