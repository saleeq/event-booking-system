from rest_framework import permissions


class IsEventCreatorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow creators of an event to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the creator of the event
        return obj.created_by == request.user
