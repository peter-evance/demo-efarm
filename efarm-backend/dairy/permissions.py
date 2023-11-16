from rest_framework.exceptions import PermissionDenied, AuthenticationFailed
from rest_framework.permissions import BasePermission


class CanAddCowBreed(BasePermission):
    """
    Custom permission class that allows farm owners and managers to add cow breeds.

    Raises:
    - `PermissionDenied`: If the user is not a farm owner or a farm manager.

    Usage:
        Add the permission class to the view or viewset that requires permission to add cow breeds:
        permission_classes = [CanAddCowBreed]
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


class CanDeleteCowBreed(BasePermission):
    """
    Custom permission class that allows farm owners and managers to delete cow breeds.

    Raises:
    - `PermissionDenied`: If the user is not a farm owner or a farm manager.

    Usage:
        Add the permission class to the view or viewset that requires permission to delete cow breeds:
        permission_classes = [CanDeleteCowBreed]
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


class CanViewCowBreeds(BasePermission):
    """
    Custom permission class that allows farm staff and workers to view cow breeds.

    Raises:
    - `PermissionDenied`: If the user is not a farm owner, a farm worker, a farm manager, or an assistant farm manager.

    Usage:
        Add the permission class to the view or viewset that requires permission to view cow breeds:
        permission_classes = [CanViewCowBreeds]
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


class CanAddCow(BasePermission):
    """
    Custom permission class that allows farm owners and managers to add new cows.

    Raises:
    - `PermissionDenied`: If the user is not a farm owner or a farm manager.

    Usage:
        Add the permission class to the view or viewset that requires permission to add cows:
        permission_classes = [CanAddCow]
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


class CanUpdateCow(BasePermission):
    """
    Custom permission class that allows farm owners and managers to update cow details.

    Raises:
    - `PermissionDenied`: If the user is not a farm owner or a farm manager.

    Usage:
        Add the permission class to the view or viewset that requires permission to update cow details:
        permission_classes = [CanUpdateCow]
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


class CanDeleteCow(BasePermission):
    """
    Custom permission class that allows farm owners to delete cows.

    Raises:
    - `PermissionDenied`: If the user is not a farm owner.

    Usage:
        Add the permission class to the view or viewset that requires permission to delete cows:
        permission_classes = [CanDeleteCow]
    """

    message = {"message": "Only farm owners have permission to perform this action."}

    def has_permission(self, request, view):
        """
        Check if the current user is a farm owner.

        Returns:
            bool: True if the user is a farm owner, otherwise raises PermissionDenied.
        """
        if request.user.is_authenticated and request.user.is_farm_owner:
            return True
        if not request.user.is_authenticated:
            raise AuthenticationFailed(
                {"message": "Authentication credentials were not provided."}
            )
        raise PermissionDenied(self.message)


class CanViewCow(BasePermission):
    """
    Custom permission class that allows farm staff and workers to view cow details.

    Raises:
    - `PermissionDenied`: If the user is not a farm owner, a farm worker, a farm manager, or an assistant farm manager.

    Usage:
        Add the permission class to the view or viewset that requires permission to view cow details:
        permission_classes = [CanViewCow]
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


class CanAddHeatRecord(BasePermission):
    message = {
        "message": "Only farm staff and workers have permission to view heat records."
    }

    def has_permission(self, request, view):
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


class CanViewHeatRecord(BasePermission):
    message = {
        "message": "Only farm staff and workers have permission to view heat records."
    }

    def has_permission(self, request, view):
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


class CanUpdateAndDeleteHeatRecord(BasePermission):
    message = {
        "message": "Only management have permission to update and delete heat records."
    }

    def has_permission(self, request, view):
        if request.user.is_authenticated and (
            request.user.is_farm_owner
            or request.user.is_farm_manager
            or request.user.is_assistant_farm_manager
        ):
            return True
        if not request.user.is_authenticated:
            raise AuthenticationFailed(
                {"message": "Authentication credentials were not provided."}
            )
        raise PermissionDenied(self.message)


class CanActOnInseminatorRecord(BasePermission):
    message = {
        "message": "Only farm owners and managers have permission to perform this action."
    }

    def has_permission(self, request, view):
        if request.user.is_authenticated and (
            request.user.is_farm_owner
            or request.user.is_farm_manager
            or request.user.is_assistant_farm_manager
        ):
            return True
        if not request.user.is_authenticated:
            raise AuthenticationFailed(
                {"message": "Authentication credentials were not provided."}
            )
        raise PermissionDenied(self.message)


class CanActOnInseminationRecord(BasePermission):
    message = {
        "message": "Only farm owners and managers have permission to perform this action."
    }

    def has_permission(self, request, view):
        if request.user.is_authenticated and (
            request.user.is_farm_owner
            or request.user.is_farm_manager
            or request.user.is_assistant_farm_manager
        ):
            return True
        if not request.user.is_authenticated:
            raise AuthenticationFailed(
                {"message": "Authentication credentials were not provided."}
            )
        raise PermissionDenied(self.message)


class CanAddPregnancyRecord(BasePermission):
    message = {
        "message": "Only farm owners and managers have permission to add pregnancy records."
    }

    def has_permission(self, request, view):
        if request.user.is_authenticated and (
            request.user.is_farm_owner or request.user.is_farm_manager
        ):
            return True
        if not request.user.is_authenticated:
            raise AuthenticationFailed(
                {"message": "Authentication credentials were not provided."}
            )
        raise PermissionDenied(self.message)


class CanViewPregnancyRecord(BasePermission):
    message = {"message": "Only farm staff have permission to view pregnancy records."}

    def has_permission(self, request, view):
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


class CanUpdatePregnancyRecord(BasePermission):
    message = {
        "message": "Only farm managers have permission to update pregnancy records."
    }

    def has_permission(self, request, view):
        if request.user.is_authenticated and (
            request.user.is_farm_owner
            or request.user.is_farm_manager
            or request.user.is_assistant_farm_manager
        ):
            return True
        if not request.user.is_authenticated:
            raise AuthenticationFailed(
                {"message": "Authentication credentials were not provided."}
            )
        raise PermissionDenied(self.message)


class CanDeletePregnancyRecord(BasePermission):
    message = {
        "message": "Only farm owners and managers have permission to delete pregnancy records."
    }

    def has_permission(self, request, view):
        if request.user.is_authenticated and (
            request.user.is_farm_owner or request.user.is_farm_manager
        ):
            return True
        if not request.user.is_authenticated:
            raise AuthenticationFailed(
                {"message": "Authentication credentials were not provided."}
            )
        raise PermissionDenied(self.message)


class CanAddLactationRecord(BasePermission):
    message = {
        "message": "Only farm owners and managers have permission to add lactation records."
    }

    def has_permission(self, request, view):
        if request.user.is_authenticated and (
            request.user.is_farm_owner or request.user.is_farm_manager
        ):
            return True
        if not request.user.is_authenticated:
            raise AuthenticationFailed(
                {"message": "Authentication credentials were not provided."}
            )
        raise PermissionDenied(self.message)


class CanViewLactationRecord(BasePermission):
    message = {"message": "Only farm staff have permission to view pregnancy records."}

    def has_permission(self, request, view):
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


class CanDeleteLactationRecord(BasePermission):
    message = {
        "message": "Only farm owners and managers have permission to delete lactation records."
    }

    def has_permission(self, request, view):
        if request.user.is_authenticated and (
            request.user.is_farm_owner or request.user.is_farm_manager
        ):
            return True
        if not request.user.is_authenticated:
            raise AuthenticationFailed(
                {"message": "Authentication credentials were not provided."}
            )
        raise PermissionDenied(self.message)


class CanAddMilk(BasePermission):
    message = {"message": "Only farm staff have permission to add milk records."}

    def has_permission(self, request, view):
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


class CanViewMilk(BasePermission):
    message = {"message": "Only farm management have permission to view milk records."}

    def has_permission(self, request, view):
        if request.user.is_authenticated and (
            request.user.is_farm_owner
            or request.user.is_farm_manager
            or request.user.is_assistant_farm_manager
        ):
            return True
        if not request.user.is_authenticated:
            raise AuthenticationFailed(
                {"message": "Authentication credentials were not provided."}
            )
        raise PermissionDenied(self.message)


class CanUpdateMilk(BasePermission):
    message = {
        "message": "Only farm management have permission to update milk records."
    }

    def has_permission(self, request, view):
        if request.user.is_authenticated and (
            request.user.is_farm_owner or request.user.is_farm_manager
        ):
            return True
        if not request.user.is_authenticated:
            raise AuthenticationFailed(
                {"message": "Authentication credentials were not provided."}
            )
        raise PermissionDenied(self.message)


class CanDeleteMilk(BasePermission):
    message = {
        "message": "Only farm management have permission to delete milk records."
    }

    def has_permission(self, request, view):
        if request.user.is_authenticated and (
            request.user.is_farm_owner or request.user.is_farm_manager
        ):
            return True
        if not request.user.is_authenticated:
            raise AuthenticationFailed(
                {"message": "Authentication credentials were not provided."}
            )
        raise PermissionDenied(self.message)


class CanActOnWeightRecord(BasePermission):
    message = {
        "message": "Only farm owners and managers have permission to perform this action."
    }

    def has_permission(self, request, view):
        if request.user.is_authenticated and (
            request.user.is_farm_owner
            or request.user.is_farm_manager
            or request.user.is_assistant_farm_manager
        ):
            return True
        if not request.user.is_authenticated:
            raise AuthenticationFailed(
                {"message": "Authentication credentials were not provided."}
            )
        raise PermissionDenied(self.message)


class CanActOnCullingRecord(BasePermission):
    message = {
        "message": "Only farm owners and farm manager have permission to perform this action."
    }

    def has_permission(self, request, view):
        if request.user.is_authenticated and (
            request.user.is_farm_owner or request.user.is_farm_manager
        ):
            return True
        if not request.user.is_authenticated:
            raise AuthenticationFailed(
                {"message": "Authentication credentials were not provided."}
            )
        raise PermissionDenied(self.message)


class CanActOnQuarantineRecord(BasePermission):
    message = {
        "message": "Only farm owners and farm managers have permission to perform this action."
    }

    def has_permission(self, request, view):
        if request.user.is_authenticated and (
            request.user.is_farm_owner or request.user.is_farm_manager
        ):
            return True
        if not request.user.is_authenticated:
            raise AuthenticationFailed(
                {"message": "Authentication credentials were not provided."}
            )
        raise PermissionDenied(self.message)


class CanActOnBarn(BasePermission):
    message = {
        "message": "Only farm owners and farm managers have permission to perform this action."
    }

    def has_permission(self, request, view):
        if request.user.is_authenticated and (
                request.user.is_farm_owner or request.user.is_farm_manager
        ):
            return True
        if not request.user.is_authenticated:
            raise AuthenticationFailed(
                {"message": "Authentication credentials were not provided."}
            )
        raise PermissionDenied(self.message)


class CanActOnCowPen(BasePermission):
    message = {
        "message": "Only farm owners and farm managers have permission to perform this action."
    }

    def has_permission(self, request, view):
        if request.user.is_authenticated and (
                request.user.is_farm_owner or request.user.is_farm_manager
        ):
            return True
        if not request.user.is_authenticated:
            raise AuthenticationFailed(
                {"message": "Authentication credentials were not provided."}
            )
        raise PermissionDenied(self.message)


class CanActOnCowInPenMovement(BasePermission):
    message = {
        "message": "Only farm owners and farm managers have permission to perform this action."
    }

    def has_permission(self, request, view):
        if request.user.is_authenticated and (
                request.user.is_farm_owner or request.user.is_farm_manager
        ):
            return True
        if not request.user.is_authenticated:
            raise AuthenticationFailed(
                {"message": "Authentication credentials were not provided."}
            )
        raise PermissionDenied(self.message)
