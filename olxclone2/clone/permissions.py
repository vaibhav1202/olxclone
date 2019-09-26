from rest_framework import permissions
class MySuperOrReadOnlyPers(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_superuser               
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True 
        return request.user.is_superuser    

class MyObjPer(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return request.user.is_superuser or obj.user.id == request.user.id
 
class MyUserPers(permissions.IsAdminUser):    
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        return request.user.is_superuser    
