from rest_framework import permissions
from django.contrib.contenttypes.models import ContentType
from users.models import GranularPermission

class HasGranularPermission(permissions.BasePermission):
    """
    Checks if the user has a GranularPermission for the requested action and model.
    Superusers and ADMINs always have permission.
    """
    
    def get_action_flag(self, request):
        if request.method in permissions.SAFE_METHODS:
            return 'can_view'
        elif request.method == 'POST':
            return 'can_add'
        elif request.method in ['PUT', 'PATCH']:
            return 'can_change'
        elif request.method == 'DELETE':
            return 'can_delete'
        return None

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
            
        if request.user.is_superuser or request.user.role == 'ADMIN':
            return True
            
        action_flag = self.get_action_flag(request)
        if not action_flag:
            return False
            
        # Get the model class from the view's queryset
        if not hasattr(view, 'get_queryset'):
            return False
            
        try:
            model_cls = view.get_queryset().model
        except Exception:
            return False
            
        content_type = ContentType.objects.get_for_model(model_cls)
        
        # Check if the user has a global permission for this model, or ANY object-level permission for this model
        # If they only have object-level, we still allow `has_permission` so `has_object_permission` can run.
        # But for POST (can_add), it must be a global permission since there's no object yet.
        
        if request.method == 'POST':
            return GranularPermission.objects.filter(
                user=request.user,
                content_type=content_type,
                object_id__isnull=True,
                **{action_flag: True}
            ).exists()
            
        # For other methods, they need either global or at least one object-level permission
        return GranularPermission.objects.filter(
            user=request.user,
            content_type=content_type,
            **{action_flag: True}
        ).exists()

    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
            
        if request.user.is_superuser or request.user.role == 'ADMIN':
            return True
            
        action_flag = self.get_action_flag(request)
        if not action_flag:
            return False
            
        content_type = ContentType.objects.get_for_model(obj)
        
        # Check if they have a global permission OR a specific object permission
        has_global = GranularPermission.objects.filter(
            user=request.user,
            content_type=content_type,
            object_id__isnull=True,
            **{action_flag: True}
        ).exists()
        
        if has_global:
            return True
            
        has_object = GranularPermission.objects.filter(
            user=request.user,
            content_type=content_type,
            object_id=obj.pk,
            **{action_flag: True}
        ).exists()
        
        return has_object


class HasGranularPermissionOrReadOnly(HasGranularPermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return super().has_object_permission(request, view, obj)

class IsCustomerOrHasGranularPermission(HasGranularPermission):
    """
    Customers bypass the GranularPermission checks (since they are limited to their own data via get_queryset).
    Staff must pass the GranularPermission check.
    """
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated and request.user.role == 'CUSTOMER':
            return True
        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_authenticated and request.user.role == 'CUSTOMER':
            return True
        return super().has_object_permission(request, view, obj)

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (request.user.role == 'ADMIN' or request.user.is_superuser)

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated and (request.user.role == 'ADMIN' or request.user.is_superuser)

class IsCustomerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role in ['CUSTOMER', 'ADMIN']

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'ADMIN' or request.user.is_superuser:
            return True
        return hasattr(obj, 'user') and obj.user == request.user
