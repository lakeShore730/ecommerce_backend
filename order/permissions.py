from rest_framework import permissions


class OrderAccessPermission(permissions.BasePermission):  
    def has_object_permission(self, request, view, obj):
        return request.user.id == obj.user.id


class OrderItemAccessPermission(permissions.BasePermission):  
    def has_object_permission(self, request, view, obj):
        return request.user.id == obj.order.user.id


