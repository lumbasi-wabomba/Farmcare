from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'owner'
    
class IsAdminOrOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['owner', 'admin']
    
class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['admin']
    
class IsSalesClerk(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['sales_clerk']
    
class IsSalesClerkOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['admin', 'sales_clerk']
    
    