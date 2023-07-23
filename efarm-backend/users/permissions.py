from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission


class IsFarmOwner(BasePermission):
    """
    Custom permission class that allows only farm owners to perform an action.

    Raises:
    - `PermissionDenied`: If the user is not a farm owner.

    Usage:
        Add the permission class to the view or viewset that requires farm owners access:
        permission_classes = [IsFarmOwner]
    """

    message = {"message": "Only farm owners have permission to perform this action."}

    def has_permission(self, request, view):
        # Check if the current user is a farm owner
        if request.user.is_authenticated and request.user.is_farm_owner:
            return True
        raise PermissionDenied(self.message)


class IsFarmManager(BasePermission):
    """
    Custom permission class that allows only farm owners and managers to perform an action.

    Raises:
    - `PermissionDenied`: If the user is not a farm owner or a farm manager.

    Usage:
        Add the permission class to the view or viewset that requires farm owners and managers access:
        permission_classes = [IsFarmManager]
    """
    message = {"message": "Only farm owners and managers have permission to perform this action."}

    def has_permission(self, request, view):
        # Check if the current user is a farm manager
        if request.user.is_authenticated and (request.user.is_farm_manager or request.user.is_farm_owner):
            return True
        raise PermissionDenied(self.message)


class IsAssistantFarmManager(BasePermission):
    """
    Custom permission class that allows only farm owners, managers, and assistants to perform an action.

    Raises:
    - `PermissionDenied`: If the user is not a farm owner, a farm manager, or an assistant farm manager.

    Usage:
        Add the permission class to the view or viewset that requires farm owners, managers, and assistants access:
        permission_classes = [IsAssistantFarmManager]
    """
    message = {"message": "Only farm owners, managers, and assistants have permission to perform this action."}

    def has_permission(self, request, view):
        # Check if the current user is an assistant farm manager
        if request.user.is_authenticated and (request.user.is_assistant_farm_manager or request.user.is_farm_manager
                                              or request.user.is_farm_owner):
            return True
        raise PermissionDenied(self.message)


class IsFarmWorker(BasePermission):
    """
    Custom permission class that allows only farm staff and workers to perform an action.

    Raises:
    - `PermissionDenied`: If the user is not a farm owner, a farm worker, a farm manager, or an assistant farm manager.

    Usage:
        Add the permission class to the view or viewset that requires farm workers access:
        permission_classes = [IsFarmWorker]
    """
    message = {"message": "Only farm staff and workers have permission to perform this action."}

    def has_permission(self, request, view):
        # Check if the current user is a farm worker
        if request.user.is_authenticated and (request.user.is_farm_owner or request.user.is_farm_worker or
                                              request.user.is_farm_manager or request.user.is_assistant_farm_manager):
            return True
        raise PermissionDenied(self.message)


class IsTeamLeader(BasePermission):
    """
    Custom permission class that allows only team leaders to perform an action.

    Raises:
    - `PermissionDenied`: If the user is not a team leader, an assistant farm manager, a farm manager, or a farm owner.

    Usage:
        Add the permission class to the view or viewset that requires team leaders access:
        permission_classes = [IsTeamLeader]
    """
    message = {"message": "Only team leaders have permission to perform this action."}

    def has_permission(self, request, view):
        # Check if the current user is a team leader
        if request.user.is_authenticated and (request.user.is_team_leader or request.user.is_assistant_farm_manager
                                              or request.user.is_farm_manager or request.user.is_farm_owner):
            return True
        raise PermissionDenied(self.message)
