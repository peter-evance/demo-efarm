from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from phonenumber_field.serializerfields import PhoneNumberField

User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    """
    Custom serializer for creating user instances with additional fields.

    Fields:
    - `phone_number`: A PhoneNumberField representing the user's phone number.
                      It is a unique field that stores phone numbers in a standardized format.
                      The phone number is validated by the Django phone number package.

    Meta:
    - `model`: The User model for which the serializer is defined.
    - `fields`: The fields to include in the serialized representation when creating a user instance.
                It includes the standard UserCreateSerializer fields along with 'phone_number'
                and additional fields representing the user's roles.

    Usage:
        Use this serializer when creating a new user instance and passing the phone number field.
        The 'phone_number' field should be in a valid phone number format, for example: '+1234567890'.
        For example:
        ```
        {
            "username": "example_user",
            "password": "password123",
            "first_name": "Peter",
            "last_name": "Evance",
            "phone_number": "+1234567890",
            "sex": "Male",
            "is_farm_owner": True,
            "is_farm_manager": False,
            "is_assistant_farm_manager": False,
            "is_team_leader": False,
            "is_farm_worker": False
        }
        ```

    """
    phone_number = PhoneNumberField()

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'phone_number', 'sex',
                  'is_farm_owner', 'is_farm_manager', 'is_assistant_farm_manager', 'is_team_leader', 'is_farm_worker')


class CustomUserSerializer(UserSerializer):
    """
    Custom serializer for retrieving and updating user instances with additional fields.

    Fields:
    - `phone_number`: A PhoneNumberField representing the user's phone number.
                      It is a unique field that stores phone numbers in a standardized format.
                      The phone number is validated by the Django phone number package.

    Meta:
    - `model`: The User model for which the serializer is defined.
    - `fields`: The fields to include in the serialized representation when retrieving or updating a user instance.
                It includes the standard UserSerializer fields along with 'phone_number'
                and additional fields representing the user's roles.

    Usage:
        Use this serializer when retrieving or updating an existing user instance.
        The 'phone_number' field can be used to retrieve or update the user's phone number.
        The 'phone_number' field should be in a valid phone number format, for example: '+1234567890'.
        For example:
        ```
        {
            "id": 1,
            "username": "example_user",
            "first_name": "Peter",
            "last_name": "Evance",
            "phone_number": "+1234567890",
            "sex": "Male",
            "is_farm_owner": True,
            "is_farm_manager": False,
            "is_assistant_farm_manager": False,
            "is_team_leader": False,
            "is_farm_worker": False
        }
        ```

    """
    phone_number = PhoneNumberField()

    class Meta(UserSerializer.Meta):
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'phone_number', 'sex', 'is_farm_owner', 'is_farm_manager'
                  , 'is_assistant_farm_manager', 'is_team_leader', 'is_farm_worker')
