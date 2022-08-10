from rest_framework import permissions


class UserAccessPermission(permissions.BasePermission):  
    def has_object_permission(self, request, view, obj):
        return request.user.id == obj.id


