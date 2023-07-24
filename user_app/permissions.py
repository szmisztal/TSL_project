from rest_framework.permissions import BasePermission

class IsLogistician(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="Logisticians group").exists()

class IsDispatcher(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="Dispatchers group").exists()

class IsDriver(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="Drivers group").exists()
