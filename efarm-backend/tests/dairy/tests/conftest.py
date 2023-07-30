import pytest
from datetime import date, timedelta
from dairy.models import *

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from users.choices import *

User = get_user_model()


@pytest.fixture()
@pytest.mark.django_db
def setup_users():
    client = APIClient()

    # Create farm owner user
    farm_owner_data = {
        'username': 'owner@example.com',
        'password': 'testpassword',
        'first_name': 'Farm',
        'last_name': 'Owner',
        'phone_number': '+254787654321',
        'sex': SexChoices.MALE,
        'is_farm_owner': True,
    }
    farm_owner_login_data = {
        'username': 'owner@example.com',
        'password': 'testpassword',
    }
    response = client.post('/auth/users/', farm_owner_data)
    assert response.status_code == status.HTTP_201_CREATED
    farm_owner_user_id = response.data['id']
    farm_owner_user_username = response.data['username']

    # Retrieve the token after login
    response = client.post(reverse('users:login'), farm_owner_login_data)
    assert response.status_code == status.HTTP_200_OK
    farm_owner_token = response.data['auth_token']

    # Create farm manager user
    farm_manager_data = {
        'username': 'manager@example.com',
        'password': 'testpassword',
        'first_name': 'Farm',
        'last_name': 'Manager',
        'phone_number': '+254755555555',
        'sex': SexChoices.MALE,
        'is_farm_manager': True,
    }
    farm_manager_login_data = {
        'username': 'manager@example.com',
        'password': 'testpassword'
    }
    response = client.post('/auth/users/', farm_manager_data)
    assert response.status_code == status.HTTP_201_CREATED
    farm_manager_user_id = response.data['id']
    farm_manager_user_username = response.data['username']

    # Retrieve the token after login
    response = client.post(reverse('users:login'), farm_manager_login_data)
    assert response.status_code == status.HTTP_200_OK
    farm_manager_token = response.data['auth_token']

    # Create assistant farm manager user
    asst_farm_manager_data = {
        'username': 'assistant@example.com',
        'password': 'testpassword',
        'first_name': 'Assistant',
        'last_name': 'Farm Manager',
        'phone_number': '+254744444444',
        'sex': SexChoices.FEMALE,
        'is_assistant_farm_manager': True,
    }
    asst_farm_manager_login_data = {
        'username': 'assistant@example.com',
        'password': 'testpassword',
    }
    response = client.post('/auth/users/', asst_farm_manager_data)
    assert response.status_code == status.HTTP_201_CREATED
    asst_farm_manager_user_id = response.data['id']
    asst_farm_manager_user_username = response.data['username']

    # Retrieve the token after login
    response = client.post(reverse('users:login'), asst_farm_manager_login_data)
    assert response.status_code == status.HTTP_200_OK
    asst_farm_manager_token = response.data['auth_token']

    # Create team leader user
    team_leader_data = {
        'username': 'leader@example.com',
        'password': 'testpassword',
        'first_name': 'Team',
        'last_name': 'Leader',
        'phone_number': '+254733333333',
        'sex': SexChoices.MALE,
        'is_team_leader': True,
    }
    team_leader_login_data = {
        'username': 'leader@example.com',
        'password': 'testpassword'
    }
    response = client.post('/auth/users/', team_leader_data)
    assert response.status_code == status.HTTP_201_CREATED
    team_leader_user_id = response.data['id']
    team_leader_user_username = response.data['username']

    # Retrieve the token after login
    response = client.post(reverse('users:login'), team_leader_login_data)
    assert response.status_code == status.HTTP_200_OK
    team_leader_token = response.data['auth_token']

    # Create farm worker user
    farm_worker_data = {
        'username': 'worker@example.com',
        'password': 'testpassword',
        'first_name': 'Farm',
        'last_name': 'Worker',
        'phone_number': '+254722222222',
        'sex': SexChoices.FEMALE,
        'is_farm_worker': True,
    }
    farm_worker_login_data = {
        'username': 'worker@example.com',
        'password': 'testpassword',
    }
    response = client.post('/auth/users/', farm_worker_data)
    assert response.status_code == status.HTTP_201_CREATED
    farm_worker_user_id = response.data['id']
    farm_worker_user_username = response.data['username']

    # Retrieve the token after login
    response = client.post(reverse('users:login'), farm_worker_login_data)
    assert response.status_code == status.HTTP_200_OK
    farm_worker_token = response.data['auth_token']

    # Create regular user
    regular_user_data = {
        'username': 'test@example.com',
        'password': 'testpassword',
        'first_name': 'John',
        'last_name': 'Doe',
        'phone_number': '+254712345678',
        'sex': SexChoices.MALE,
    }
    regular_user_login_data = {
        'username': 'test@example.com',
        'password': 'testpassword',
    }

    response = client.post('/auth/users/', regular_user_data)
    assert response.status_code == status.HTTP_201_CREATED
    regular_user_id = response.data['id']
    regular_user_username = response.data['username']

    # Retrieve the token after login
    response = client.post(reverse('users:login'), regular_user_login_data)
    assert response.status_code == status.HTTP_200_OK
    regular_user_token = response.data['auth_token']

    return {
        'client': client,

        'regular_user_id': regular_user_id,
        'regular_user_token': regular_user_token,
        'regular_user_username': regular_user_username,

        'farm_owner_token': farm_owner_token,
        'farm_owner_user_id': farm_owner_user_id,
        'farm_owner_user_username': farm_owner_user_username,

        'farm_manager_token': farm_manager_token,
        'farm_manager_user_id': farm_manager_user_id,
        'farm_manager_user_username': farm_manager_user_username,

        'asst_farm_manager_token': asst_farm_manager_token,
        'asst_farm_manager_user_id': asst_farm_manager_user_id,
        'asst_farm_manager_user_username': asst_farm_manager_user_username,

        'team_leader_token': team_leader_token,
        'team_leader_user_id': team_leader_user_id,
        'team_leader_user_username': team_leader_user_username,

        'farm_worker_token': farm_worker_token,
        'farm_worker_user_id': farm_worker_user_id,
        'farm_worker_user_username': farm_worker_user_username,
    }


@pytest.fixture
def setup_cows():
    """
    Fixture to create a sample cows object for testing.
    """

    general_cow = {
        'name': 'General Cow',
        'breed': {'name': CowBreedChoices.AYRSHIRE},
        'date_of_birth': todays_date - timedelta(days=300),
        'gender': SexChoices.FEMALE,
        'availability_status': CowAvailabilityChoices.ALIVE,
        'current_pregnancy_status': CowPregnancyChoices.UNAVAILABLE,
        'category': CowCategoryChoices.HEIFER,
        'current_production_status': CowProductionStatusChoices.YOUNG_HEIFER,
    }

    return general_cow


@pytest.fixture
def mature_open_female_cow():
    cow_data = {
        'name': 'Mature Female Cow',
        'breed': BreedChoices.GUERNSEY,
        'date_of_birth': date.today() - timedelta(days=356 * 3),  # Adjust the age to make it mature
        'gender': SexChoices.FEMALE,
        'availability_status': CowAvailabilityChoices.ALIVE,
        'pregnancy_status': CowPregnancyChoices.OPEN,
    }
    cow = Cow.objects.create(**cow_data)
    return cow


@pytest.fixture
def calf_with_parents():
    dam_data = {
        'name': 'Mature Female Cow',
        'breed': BreedChoices.GUERNSEY,
        'date_of_birth': date.today() - timedelta(days=356 * 3),
        'gender': SexChoices.FEMALE,
        'availability_status': CowAvailabilityChoices.ALIVE,
        'pregnancy_status': CowPregnancyChoices.OPEN,
    }
    dam: Cow = Cow.objects.create(**dam_data)

    sire_data = {
        'name': 'Mature Male Cow',
        'breed': BreedChoices.AYRSHIRE,
        'date_of_birth': date.today() - timedelta(days=356 * 3),
        'gender': SexChoices.MALE,
        'availability_status': CowAvailabilityChoices.ALIVE,
        'pregnancy_status': CowPregnancyChoices.UNAVAILABLE,
    }
    sire: Cow = Cow.objects.create(**sire_data)

    calf_data = {
        'name': 'Young Female Calf',
        'breed': BreedChoices.GUERNSEY,
        'date_of_birth': date.today() - timedelta(days=50),
        'availability_status': CowAvailabilityChoices.ALIVE,
        'pregnancy_status': CowPregnancyChoices.UNAVAILABLE,
        # 'dam': dam,
        'sire': sire
    }
    calf: Cow = Cow.objects.create(**calf_data)

    return calf

# @pytest.fixture
# def mature_male_cow():
#     cow_data = {
#         'name': 'Mature Male Cow',
#         'breed': BreedChoices.FRIESIAN,
#         'date_of_birth': date.today() - timedelta(days=365*2),  # Adjust the age to make it mature
#         'gender': SexChoices.MALE,
#         'availability_status': CowAvailabilityChoices.ALIVE,
#         'pregnancy_status': CowPregnancyChoices.UNAVAILABLE,
#     }
#     cow = Cow(**cow_data)
#     cow.save()  # Save the instance to generate the ID
#     return cow
#
#
#

#
#
# @pytest.fixture
# def calf_cow():
#     cow_data = {
#         'name': 'Calf Cow',
#         'breed': BreedChoices.GUERNSEY,
#         'date_of_birth': date.today() - timedelta(days=100),  # Adjust the age to make it a calf
#         'gender': SexChoices.FEMALE,
#         'availability_status': CowAvailabilityChoices.ALIVE,
#         'pregnancy_status': CowPregnancyChoices.OPEN,
#     }
#     cow = Cow.objects.create(**cow_data)
#     return cow
