from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAdminUser, IsAuthenticated 
from product.models import Product
from .models import Order, Item
from .serializers import OrderCreationSerializer, OrderSerializer, ItemSerializer, OrderListSerializer
from .pagination import CustomPagination
from .permissions import OrderAccessPermission, OrderItemAccessPermission

class OrderViewSet(viewsets.ViewSet):
    permission_classes_by_action = {
        'list': [IsAuthenticated], 
        'retrieve': [OrderAccessPermission],
        'create': [IsAuthenticated],
        'update': [IsAdminUser],
        'partial_update': [OrderAccessPermission],
        'destroy': [IsAdminUser]
    }
    
    def list(self, request):
        paginator = CustomPagination()
        queryset = Order.objects.filter(user=request.user)
        context = paginator.paginate_queryset(queryset, request)
        serializer = OrderSerializer(context, many=True)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request):
        order_creation_serializer = OrderCreationSerializer(data=request.data)
        order_creation_serializer.is_valid(raise_exception=True)
       
        product_queryset = Product.objects.all()
        selected_products = []
        total_amount = 0

        for item in order_creation_serializer.data['items']:
            product = get_object_or_404(product_queryset, pk=item['product'])
            selected_products.append(product)
            total_amount += (product.price * item['quantity']) - product.discount
        
        order_details = {
            'user': request.user.id,
            'total_amount': total_amount,
            'remarks': order_creation_serializer.data['remarks']
        }

        order_serializer = OrderSerializer(data=order_details)
        order_serializer.is_valid(raise_exception=True)
        order_serializer.save()

        for i, product in enumerate(selected_products):
            
            item_details = {
                'order': order_serializer.data['id'],
                'product': product.id,
                'price': product.price,
                'name': product.name,
                'discount': product.discount,
                'quantity': order_creation_serializer.data['items'][i]['quantity']
            }

            item_serializer = ItemSerializer(data=item_details)
            item_serializer.is_valid(raise_exception=True)
            item_data = item_serializer.save()
    
        return Response(order_serializer.data)
    
    def retrieve(self, request, pk=None):
        queryset = Order.objects.all()
        order = get_object_or_404(queryset, pk=pk)
        serializer = OrderListSerializer(order)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        queryset = Order.objects.all()
        order = get_object_or_404(queryset, pk=pk)
        self.check_object_permissions(request, order) # Applying the object level permission checking
        serializer = OrderSerializer(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        order_list_serializer = OrderListSerializer(order)
        return Response(order_list_serializer.data)

    # Applying permission classes based on per viewSet method 
    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]


class OrderItemViewSet(viewsets.ViewSet):
    permission_classes_by_action = {
        'retrieve': [OrderItemAccessPermission],
    }
    
    def retrieve(self, request, pk=None):
        queryset = Item.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        self.check_object_permissions(request, item)
        serializer = ItemSerializer(item)
        return Response(serializer.data)

    # Applying permission classes based on per viewSet method
    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]