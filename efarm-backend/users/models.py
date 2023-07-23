from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from phonenumber_field.modelfields import PhoneNumberField

from users.choices import *
from users.validators import *


class CustomUser(AbstractUser):
    """
        Custom user model representing a user in the farm management system.

        Fields:
        - `username`: A unique character field representing the username of the user.
                      It is limited to a maximum length of 45 characters.
        - `first_name`: A character field representing the first name of the user.
                         It is limited to a maximum length of 20 characters.
        - `last_name`: A character field representing the last name of the user.
                        It is limited to a maximum length of 20 characters.
        - `phone_number`: A phone number field representing the phone number of the user.
                          It is limited to a maximum length of 13 characters and must be unique.
        - `sex`: A character field representing the gender of the user.
                 The available choices are defined in the `SexChoices` enum.
                 It is limited to a maximum length of 6 characters.
        - `is_farm_owner`: A boolean field representing whether the user is a farm owner.
        - `is_farm_manager`: A boolean field representing whether the user is a farm manager.
        - `is_assistant_farm_manager`: A boolean field representing whether the user is an assistant farm manager.
        - `is_team_leader`: A boolean field representing whether the user is a team leader.
        - `is_farm_worker`: A boolean field representing whether the user is a farm worker.

        Methods:
        - `assign_farm_owner()`: Assigns the user as a farm owner and updates related fields accordingly.
        - `assign_farm_manager()`: Assigns the user as a farm manager and updates related fields accordingly.
        - `assign_assistant_farm_manager()`: Assigns the user as an assistant farm manager and updates related fields accordingly.
        - `assign_team_leader()`: Assigns the user as a team leader and updates related fields accordingly.
        - `assign_farm_worker()`: Assigns the user as a farm worker and updates related fields accordingly.
        - `dismiss_farm_owner()`: Dismisses the user from the farm owner role.
        - `dismiss_farm_manager()`: Dismisses the user from the farm manager role.
        - `dismiss_assistant_farm_manager()`: Dismisses the user from the assistant farm manager role.
        - `dismiss_team_leader()`: Dismisses the user from the team leader role.
        - `dismiss_farm_worker()`: Dismisses the user from the farm worker role.
        - `get_full_name()`: Returns the full name of the user.
        - `get_role()`: Returns the role of the user based on their assigned roles.
        - `get_farm_workers()`: Retrieves all farm workers associated with the user.
        - `get_team_leaders()`: Retrieves all team leaders associated with the user.
        - `get_assistant_farm_managers()`: Retrieves all assistant farm managers associated with the user.
        - `get_farm_managers()`: Retrieves all farm managers associated with the user.
        - `get_farm_owners()`: Retrieves all farm owners associated with the user.
        - `generate_username(first_name, last_name)`: Generates a unique username based on the user's first name and last name.

        """
    username = models.CharField(max_length=45, unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone_number = PhoneNumberField(max_length=13, unique=True)
    sex = models.CharField(choices=SexChoices.choices, max_length=6)
    is_farm_owner = models.BooleanField(default=False)
    is_farm_manager = models.BooleanField(default=False)
    is_assistant_farm_manager = models.BooleanField(default=False)
    is_team_leader = models.BooleanField(default=False)
    is_farm_worker = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number', 'sex']

    def assign_farm_owner(self):
        self.is_farm_owner = True
        self.is_farm_manager = False
        self.is_assistant_farm_manager = False
        self.is_team_leader = False
        self.is_farm_worker = False
        self.save()

    def assign_farm_manager(self):
        self.is_farm_owner = False
        self.is_farm_manager = True
        self.is_assistant_farm_manager = False
        self.is_team_leader = False
        self.is_farm_worker = False
        self.save()

    def assign_assistant_farm_manager(self):
        self.is_farm_owner = False
        self.is_farm_manager = False
        self.is_assistant_farm_manager = True
        self.is_team_leader = False
        self.is_farm_worker = False
        self.save()

    def assign_team_leader(self):
        self.is_farm_owner = False
        self.is_farm_manager = False
        self.is_assistant_farm_manager = False
        self.is_team_leader = True
        self.is_farm_worker = True
        self.save()

    def assign_farm_worker(self):
        self.is_farm_owner = False
        self.is_farm_manager = False
        self.is_asst_farm_manager = False
        self.is_team_leader = False
        self.is_farm_worker = True
        self.save()

    def dismiss_farm_owner(self):
        self.is_farm_owner = False
        self.save()

    def dismiss_farm_manager(self):
        self.is_farm_manager = False
        self.save()

    def dismiss_assistant_farm_manager(self):
        self.is_assistant_farm_manager = False
        self.save()

    def dismiss_team_leader(self):
        self.is_team_leader = False
        self.save()

    def dismiss_farm_worker(self):
        self.is_farm_worker = False
        self.save()

    def get_full_name(self):
        """Return the full name of the user."""
        return f"{self.first_name} {self.last_name}"

    def get_role(self):
        """Return the role of the user."""
        if self.is_farm_owner:
            return "Farm Owner"
        elif self.is_farm_manager:
            return "Farm Manager"
        elif self.is_assistant_farm_manager:
            return "Assistant Farm Manager"
        elif self.is_team_leader:
            return "Team Leader"
        elif self.is_farm_worker:
            return "Farm Worker"
        else:
            return "Regular User"

    def get_farm_workers(self):
        return CustomUser.objects.filter(is_farm_worker=True)

    def get_team_leaders(self):
        return CustomUser.objects.filter(is_team_leader=True)

    def get_assistant_farm_managers(self):
        return CustomUser.objects.filter(is_assistant_farm_manager=True)

    def get_farm_managers(self):
        return CustomUser.objects.filter(is_farm_manager=True)

    def get_farm_owners(self):
        return CustomUser.objects.filter(is_farm_owner=True)

    def clean(self):
        CustomUserValidator.validate_sex(self, self.sex)
        CustomUserValidator.validate_username(self, self.username)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def generate_username(first_name, last_name):
        base_username = slugify(f"{first_name}-{last_name}")
        username = base_username
        counter = 1

        while CustomUser.objects.filter(username=username).exists():
            username = f"{base_username}-{counter}"
            counter += 1

        return username
