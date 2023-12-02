from datetime import timedelta

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from poultry.choices import *
from poultry.serializers import *
from users.choices import *


@pytest.fixture()
@pytest.mark.django_db
def setup_users():
    client = APIClient()

    # Create farm owner user
    farm_owner_data = {
        "username": "owner@example.com",
        "password": "testpassword",
        "first_name": "Farm",
        "last_name": "Owner",
        "phone_number": "+254787654321",
        "sex": SexChoices.MALE,
        "is_farm_owner": True,
    }
    farm_owner_login_data = {
        "username": "owner@example.com",
        "password": "testpassword",
    }
    response = client.post("/auth/users/", farm_owner_data)
    assert response.status_code == status.HTTP_201_CREATED
    farm_owner_user_id = response.data["id"]
    farm_owner_user_username = response.data["username"]

    # Retrieve the token after login
    response = client.post(reverse("users:login"), farm_owner_login_data)
    assert response.status_code == status.HTTP_200_OK
    farm_owner_token = response.data["auth_token"]

    # Create farm manager user
    farm_manager_data = {
        "username": "manager@example.com",
        "password": "testpassword",
        "first_name": "Farm",
        "last_name": "Manager",
        "phone_number": "+254755555555",
        "sex": SexChoices.MALE,
        "is_farm_manager": True,
    }
    farm_manager_login_data = {
        "username": "manager@example.com",
        "password": "testpassword",
    }
    response = client.post("/auth/users/", farm_manager_data)
    assert response.status_code == status.HTTP_201_CREATED
    farm_manager_user_id = response.data["id"]
    farm_manager_user_username = response.data["username"]

    # Retrieve the token after login
    response = client.post(reverse("users:login"), farm_manager_login_data)
    assert response.status_code == status.HTTP_200_OK
    farm_manager_token = response.data["auth_token"]

    # Create assistant farm manager user
    asst_farm_manager_data = {
        "username": "assistant@example.com",
        "password": "testpassword",
        "first_name": "Assistant",
        "last_name": "Farm Manager",
        "phone_number": "+254744444444",
        "sex": SexChoices.FEMALE,
        "is_assistant_farm_manager": True,
    }
    asst_farm_manager_login_data = {
        "username": "assistant@example.com",
        "password": "testpassword",
    }
    response = client.post("/auth/users/", asst_farm_manager_data)
    assert response.status_code == status.HTTP_201_CREATED
    asst_farm_manager_user_id = response.data["id"]
    asst_farm_manager_user_username = response.data["username"]

    # Retrieve the token after login
    response = client.post(reverse("users:login"), asst_farm_manager_login_data)
    assert response.status_code == status.HTTP_200_OK
    asst_farm_manager_token = response.data["auth_token"]

    # Create team leader user
    team_leader_data = {
        "username": "leader@example.com",
        "password": "testpassword",
        "first_name": "Team",
        "last_name": "Leader",
        "phone_number": "+254733333333",
        "sex": SexChoices.MALE,
        "is_team_leader": True,
        "is_farm_worker": True,
    }
    team_leader_login_data = {
        "username": "leader@example.com",
        "password": "testpassword",
    }
    response = client.post("/auth/users/", team_leader_data)
    assert response.status_code == status.HTTP_201_CREATED
    team_leader_user_id = response.data["id"]
    team_leader_user_username = response.data["username"]

    # Retrieve the token after login
    response = client.post(reverse("users:login"), team_leader_login_data)
    assert response.status_code == status.HTTP_200_OK
    team_leader_token = response.data["auth_token"]

    # Create farm worker user
    farm_worker_data = {
        "username": "worker@example.com",
        "password": "testpassword",
        "first_name": "Farm",
        "last_name": "Worker",
        "phone_number": "+254722222222",
        "sex": SexChoices.FEMALE,
        "is_farm_worker": True,
    }
    farm_worker_login_data = {
        "username": "worker@example.com",
        "password": "testpassword",
    }
    response = client.post("/auth/users/", farm_worker_data)
    assert response.status_code == status.HTTP_201_CREATED
    farm_worker_user_id = response.data["id"]
    farm_worker_user_username = response.data["username"]

    # Retrieve the token after login
    response = client.post(reverse("users:login"), farm_worker_login_data)
    assert response.status_code == status.HTTP_200_OK
    farm_worker_token = response.data["auth_token"]

    # Create regular user
    regular_user_data = {
        "username": "test@example.com",
        "password": "testpassword",
        "first_name": "John",
        "last_name": "Doe",
        "phone_number": "+254712345678",
        "sex": SexChoices.MALE,
    }
    regular_user_login_data = {
        "username": "test@example.com",
        "password": "testpassword",
    }

    response = client.post("/auth/users/", regular_user_data)
    assert response.status_code == status.HTTP_201_CREATED
    regular_user_id = response.data["id"]
    regular_user_username = response.data["username"]

    # Retrieve the token after login
    response = client.post(reverse("users:login"), regular_user_login_data)
    assert response.status_code == status.HTTP_200_OK
    regular_user_token = response.data["auth_token"]

    return {
        "client": client,
        "regular_user_token": regular_user_token,
        "farm_owner_token": farm_owner_token,
        "farm_manager_token": farm_manager_token,
        "asst_farm_manager_token": asst_farm_manager_token,
        "team_leader_token": team_leader_token,
        "farm_worker_token": farm_worker_token,
    }


@pytest.fixture()
def setup_housing_structure_data():
    housing_structure_data = {
        "house_type": HousingStructureTypeChoices.DEEP_LITTER_HOUSE,
        "category": HousingStructureCategoryChoices.BROODER_CHICK_HOUSE,
    }
    return {"housing_structure_data": housing_structure_data}


@pytest.fixture()
def setup_flock_data():
    housing_structure_data = {
        "house_type": HousingStructureTypeChoices.DEEP_LITTER_HOUSE,
        "category": HousingStructureCategoryChoices.BROODER_CHICK_HOUSE,
    }

    serializer1 = HousingStructureSerializer(data=housing_structure_data)
    serializer1.is_valid()
    housing_structure = serializer1.save()
    flock_data = {
        "source": {"name": FlockSourceChoices.KEN_CHICK},
        "breed": {"name": FlockBreedTypeChoices.KENBRO},
        "date_of_hatching": todays_date,
        "chicken_type": ChickenTypeChoices.LAYERS,
        "initial_number_of_birds": 300,
        "current_rearing_method": RearingMethodChoices.DEEP_LITTER,
        "current_housing_structure": housing_structure.id,
    }
    return {"flock_data": flock_data}


@pytest.fixture()
@pytest.mark.django_db
def setup_flock_movement_data():
    housing_structure_data = {
        "house_type": HousingStructureTypeChoices.DEEP_LITTER_HOUSE,
        "category": HousingStructureCategoryChoices.BROODER_CHICK_HOUSE,
    }

    serializer1 = HousingStructureSerializer(data=housing_structure_data)
    serializer1.is_valid()
    housing_structure_1 = serializer1.save()

    flock_data = {
        "source": {"name": FlockSourceChoices.KEN_CHICK},
        "breed": {"name": FlockBreedTypeChoices.KENBRO},
        "date_of_hatching": todays_date,
        "chicken_type": ChickenTypeChoices.LAYERS,
        "initial_number_of_birds": 300,
        "current_rearing_method": RearingMethodChoices.DEEP_LITTER,
        "current_housing_structure": housing_structure_1.id,
    }
    serializer2 = FlockSerializer(data=flock_data)
    serializer2.is_valid()
    flock = serializer2.save()

    serializer3 = HousingStructureSerializer(data=housing_structure_data)
    serializer3.is_valid()
    housing_structure_2 = serializer3.save()

    serializer4 = HousingStructureSerializer(data=housing_structure_data)
    serializer4.is_valid()
    housing_structure_3 = serializer4.save()

    flock_movement_data = {
        "flock": flock.id,
        "from_structure": housing_structure_1.id,
        "to_structure": housing_structure_2.id,
    }

    return {
        "flock_movement_data": flock_movement_data,
        "housing_structure_3": housing_structure_3.id,
    }


@pytest.fixture()
@pytest.mark.django_db
def setup_flock_inspection_data():
    housing_structure_data = {
        "house_type": HousingStructureTypeChoices.DEEP_LITTER_HOUSE,
        "category": HousingStructureCategoryChoices.BROODER_CHICK_HOUSE,
    }

    serializer1 = HousingStructureSerializer(data=housing_structure_data)
    serializer1.is_valid()
    housing_structure = serializer1.save()

    flock_data = {
        "source": {"name": FlockSourceChoices.KEN_CHICK},
        "breed": {"name": FlockBreedTypeChoices.KENBRO},
        "date_of_hatching": todays_date - timedelta(weeks=3),
        "chicken_type": ChickenTypeChoices.LAYERS,
        "initial_number_of_birds": 300,
        "current_rearing_method": RearingMethodChoices.DEEP_LITTER,
        "current_housing_structure": housing_structure.id
    }
    serializer2 = FlockSerializer(data=flock_data)
    serializer2.is_valid()
    flock = serializer2.save()

    flock_inspection_data = {
        "flock": flock.id,
        "number_of_dead_birds": 5,
    }

    return {
        "flock_inspection_data": flock_inspection_data,
    }


@pytest.fixture()
@pytest.mark.django_db
def setup_flock_breed_information_data():
    flock_breed_data = {"name": FlockBreedTypeChoices.KENBRO}
    serializer = FlockBreedSerializer(data=flock_breed_data)
    serializer.is_valid()
    flock_breed = serializer.save()

    flock_breed_information_data = {
        "breed": flock_breed.id,
        "chicken_type": ChickenTypeChoices.LAYERS,
        "average_mature_weight_in_kgs": 2.5,
        "average_egg_production": 275,
        "maturity_age_in_weeks": 17
    }

    return {"flock_breed_information_data": flock_breed_information_data}


@pytest.fixture()
def setup_egg_collection_data():
    housing_structure_data = {
        "house_type": HousingStructureTypeChoices.DEEP_LITTER_HOUSE,
        "category": HousingStructureCategoryChoices.GROWERS_HOUSE,
    }

    serializer1 = HousingStructureSerializer(data=housing_structure_data)
    serializer1.is_valid()
    housing_structure_1 = serializer1.save()
    flock_data = {
        "source": {"name": FlockSourceChoices.KEN_CHICK},
        "breed": {"name": FlockBreedTypeChoices.KENBRO},
        "date_of_hatching": todays_date - timedelta(weeks=14),
        "chicken_type": ChickenTypeChoices.LAYERS,
        "initial_number_of_birds": 400,
        "current_rearing_method": RearingMethodChoices.DEEP_LITTER,
        "current_housing_structure": housing_structure_1.id
    }
    serializer2 = FlockSerializer(data=flock_data)
    serializer2.is_valid()
    flock = serializer2.save()

    egg_collection_data = {
        "flock": flock.id,
        "collected_eggs": 80,
        "broken_eggs": 4
    }
    return {"egg_collection_data": egg_collection_data}
