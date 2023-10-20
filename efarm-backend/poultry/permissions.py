from rest_framework.exceptions import PermissionDenied, AuthenticationFailed
from rest_framework.permissions import BasePermission


class CanAddFlockSource(BasePermission):
    """
    Custom permission class that allows farm owners and managers to add flock sources.

    Raises:
    - `PermissionDenied`: If the user is not a farm owner or a farm manager.

    Usage:
        Add the permission class to the view or viewset that requires permission to add flock sources:
        permission_classes = [CanAddFlockSource]
    """

    message = {
        "message": "Only farm owners and managers have permission to perform this action."
    }

    def has_permission(self, request, view):
        """
        Check if the current user is a farm owner or a farm manager.

        Returns:
            bool: True if the user is a farm owner or a farm manager, otherwise raises PermissionDenied.
        """
        if request.user.is_authenticated and (
                request.user.is_farm_owner or request.user.is_farm_manager
        ):
            return True
        if not request.user.is_authenticated:
            raise AuthenticationFailed(
                {"message": "Authentication credentials were not provided."}
            )
        raise PermissionDenied(self.message)


class CanDeleteFlockSource(BasePermission):
    """
    Custom permission class that allows farm owners and managers to delete flock sources.

    Raises:
    - `PermissionDenied`: If the user is not a farm owner or a farm manager.

    Usage:
        Add the permission class to the view or viewset that requires permission to delete flock sources:
        permission_classes = [CanDeleteFlockSource]
    """

    message = {
        "message": "Only farm owners and managers have permission to perform this action."
    }

    def has_permission(self, request, view):
        """
        Check if the current user is a farm owner or a farm manager.

        Returns:
            bool: True if the user is a farm owner or a farm manager, otherwise raises PermissionDenied.
        """
        if request.user.is_authenticated and (
                request.user.is_farm_owner or request.user.is_farm_manager
        ):
            return True
        if not request.user.is_authenticated:
            raise AuthenticationFailed(
                {"message": "Authentication credentials were not provided."}
            )
        raise PermissionDenied(self.message)


class CanViewFlockSource(BasePermission):
    """
    Custom permission class that allows farm staff and workers to view flock sources.

    Raises:
    - `PermissionDenied`: If the user is not a farm owner, a farm worker, a farm manager, or an assistant farm manager.

    Usage:
        Add the permission class to the view or viewset that requires permission to view flock sources:
        permission_classes = [CanViewFlockSources]
    """

    message = {
        "message": "Only farm staff and workers have permission to perform this action."
    }

    def has_permission(self, request, view):
        """
        Check if the current user is a farm owner, a farm worker, a farm manager, or an assistant farm manager.

        Returns:
            bool: True if the user has one of the allowed roles, otherwise raises PermissionDenied.
        """
        if request.user.is_authenticated and (
                request.user.is_farm_owner
                or request.user.is_farm_worker
                or request.user.is_farm_manager
                or request.user.is_assistant_farm_manager
        ):
            return True
        if not request.user.is_authenticated:
            raise AuthenticationFailed(
                {"message": "Authentication credentials were not provided."}
            )
        raise PermissionDenied(self.message)


class CanAddFlockBreed(BasePermission):
    """
    Custom permission class that allows farm owners and managers to add flock breeds.

    Raises:
    - `PermissionDenied`: If the user is not a farm owner or a farm manager.

    Usage:
        Add the permission class to the view or viewset that requires permission to add flock breeds:
        permission_classes = [CanAddFlockBreed]
    """

    message = {
        "message": "Only farm owners and managers have permission to perform this action."
    }

    def has_permission(self, request, view):
        """
        Check if the current user is a farm owner or a farm manager.

        Returns:
            bool: True if the user is a farm owner or a farm manager, otherwise raises PermissionDenied.
        """
        if request.user.is_authenticated and (
                request.user.is_farm_owner or request.user.is_farm_manager
        ):
            return True
        if not request.user.is_authenticated:
            raise AuthenticationFailed(
                {"message": "Authentication credentials were not provided."}
            )
        raise PermissionDenied(self.message)


class CanDeleteFlockBreed(BasePermission):
    """
    Custom permission class that allows farm owners and managers to delete flock breeds.

    Raises:
    - `PermissionDenied`: If the user is not a farm owner or a farm manager.

    Usage:
        Add the permission class to the view or viewset that requires permission to delete flock breeds:
        permission_classes = [CanDeleteFlockBreed]
    """

    message = {
        "message": "Only farm owners and managers have permission to perform this action."
    }

    def has_permission(self, request, view):
        """
        Check if the current user is a farm owner or a farm manager.

        Returns:
            bool: True if the user is a farm owner or a farm manager, otherwise raises PermissionDenied.
        """
        if request.user.is_authenticated and (
                request.user.is_farm_owner or request.user.is_farm_manager
        ):
            return True
        if not request.user.is_authenticated:
            raise AuthenticationFailed(
                {"message": "Authentication credentials were not provided."}
            )
        raise PermissionDenied(self.message)


class CanViewFlockBreeds(BasePermission):
    """
    Custom permission class that allows farm staff and workers to view flock breeds.

    Raises:
    - `PermissionDenied`: If the user is not a farm owner, a farm worker, a farm manager, or an assistant farm manager.

    Usage:
        Add the permission class to the view or viewset that requires permission to view flock breeds:
        permission_classes = [CanViewFlockBreeds]
    """

    message = {
        "message": "Only farm staff and workers have permission to perform this action."
    }

    def has_permission(self, request, view):
        """
        Check if the current user is a farm owner, a farm worker, a farm manager, or an assistant farm manager.

        Returns:
            bool: True if the user has one of the allowed roles, otherwise raises PermissionDenied.
        """
        if request.user.is_authenticated and (
                request.user.is_farm_owner
                or request.user.is_farm_worker
                or request.user.is_farm_manager
                or request.user.is_assistant_farm_manager
        ):
            return True
        if not request.user.is_authenticated:
            raise AuthenticationFailed(
                {"message": "Authentication credentials were not provided."}
            )
        raise PermissionDenied(self.message)
