from rest_framework.exceptions import ValidationError


class CustomUserValidator:
    """
    Helper class for validating fields in the CustomUser model.

    Methods:
    - `validate_sex(sex)`: Validates that the sex field value is within the specified choices.
    - `validate_username(username)`: Validates that the username is unique and exists in the database.

    """

    @staticmethod
    def validate_sex(sex):
        """
        Validates that the sex field value is within the specified choices.

        Parameters:
        - `sex`: The value of the sex field.

        Raises:
        - `ValidationError`: If the sex value is not within the choices or is an empty string.

        """
        from users.choices import SexChoices

        if not sex:
            raise ValidationError("Sex field cannot be empty.")

        if sex not in SexChoices.values:
            raise ValidationError(f"Invalid value for sex: '{sex}'. It must be one of {SexChoices.values}.")

    @staticmethod
    def validate_username(username):
        """
        Validates that the username is unique and exists in the database.

        Parameters:
        - `username`: The username to validate.

        Raises:
        - `ValidationError`: If the username is not unique or does not exist in the database.

        """
        from users.models import CustomUser

        if CustomUser.objects.filter(username=username).exclude(username=username).exists():
            raise ValidationError("Username already exists.")
