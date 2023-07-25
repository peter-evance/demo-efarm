import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient

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
    farm_owner_user_id = response.data['id']
    farm_owner_user_username = response.data['username']

    # Retrieve the token after login
    response = client.post(reverse('users:login'), farm_owner_login_data)
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
    farm_manager_user_id = response.data['id']
    farm_manager_user_username = response.data['username']

    # Retrieve the token after login
    response = client.post(reverse('users:login'), farm_manager_login_data)
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
    asst_farm_manager_user_id = response.data['id']
    asst_farm_manager_user_username = response.data['username']

    # Retrieve the token after login
    response = client.post(reverse('users:login'), asst_farm_manager_login_data)
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
    team_leader_user_id = response.data['id']
    team_leader_user_username = response.data['username']

    # Retrieve the token after login
    response = client.post(reverse('users:login'), team_leader_login_data)
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
    farm_worker_user_id = response.data['id']
    farm_worker_user_username = response.data['username']

    # Retrieve the token after login
    response = client.post(reverse('users:login'), farm_worker_login_data)
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
    regular_user_id = response.data['id']
    regular_user_username = response.data['username']

    # Retrieve the token after login
    response = client.post(reverse('users:login'), regular_user_login_data)
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
