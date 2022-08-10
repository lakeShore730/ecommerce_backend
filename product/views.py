from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAdminUser, AllowAny    
from .pagination import CustomPagination
from .serializers import CategorySerializer, ProductListSerializer, ProductSerializer
from .models import Category, Product

class CategoryViewSet(viewsets.ViewSet):
    permission_classes_by_action = {
        'list': [AllowAny], 
        'retrieve': [AllowAny],
        'create': [IsAdminUser],
        'update': [IsAdminUser],
        'partial_update': [IsAdminUser],
        'destroy': [IsAdminUser]
    }

    def list(self, request):
        queryset = Category.objects.all()
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Category.objects.all()
        category = get_object_or_404(queryset, pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def create(self, request):
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        queryset = Category.objects.all()
        category = get_object_or_404(queryset, pk=pk)
        serializer = CategorySerializer(category, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def destroy(self, request, pk=None):
        queryset = Category.objects.all()
        category = get_object_or_404(queryset, pk=pk)
        # Remove category reference from Product table before deleting the object
        Product.objects.exclude(category=pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # Applying permission classes based on per viewSet method
    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]


# View set for product

class ProductViewSet(viewsets.ViewSet):
    permission_classes_by_action = {
        'list': [AllowAny], 
        'retrieve': [AllowAny],
        'create': [IsAdminUser],
        'update': [IsAdminUser],
        'partial_update': [IsAdminUser],
        'destroy': [IsAdminUser]
    }
    
    def list(self, request):
        paginator = CustomPagination()
        queryset = Product.objects.all()
        context = paginator.paginate_queryset(queryset, request)
        serializer = ProductListSerializer(context, many=True)
        return paginator.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Product.objects.all()
        product = get_object_or_404(queryset, pk=pk)
        serializer = ProductListSerializer(product)
        return Response(serializer.data)

    def create(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.context['user'] = request.user
        serializer.is_valid(raise_exception=True)
        product= serializer.save()
        product_serializer = ProductListSerializer(product)
        return Response(product_serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, pk=None):
        queryset = Product.objects.all()
        product = get_object_or_404(queryset, pk=pk)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        product_serializer = ProductListSerializer(product)
        return Response(product_serializer.data)

    def destroy(self, request, pk=None):
        query_set = Product.objects.all()
        product = get_object_or_404(query_set, pk=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # Applying permission classes based on per viewSet method
    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]


