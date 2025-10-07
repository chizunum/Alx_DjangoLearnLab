from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission: allow safe methods for any request, but only owners can edit/delete.
    """

    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS are GET, HEAD, OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True
        # for Post: obj.author; for Comment: obj.author
        return getattr(obj, "author", None) == request.user
