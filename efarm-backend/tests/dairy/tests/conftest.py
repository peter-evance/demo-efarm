import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from dairy.serializers import *
from users.choices import *

User = get_user_model()


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
        "regular_user_id": regular_user_id,
        "regular_user_token": regular_user_token,
        "regular_user_username": regular_user_username,
        "farm_owner_token": farm_owner_token,
        "farm_owner_user_id": farm_owner_user_id,
        "farm_owner_user_username": farm_owner_user_username,
        "farm_manager_token": farm_manager_token,
        "farm_manager_user_id": farm_manager_user_id,
        "farm_manager_user_username": farm_manager_user_username,
        "asst_farm_manager_token": asst_farm_manager_token,
        "asst_farm_manager_user_id": asst_farm_manager_user_id,
        "asst_farm_manager_user_username": asst_farm_manager_user_username,
        "team_leader_token": team_leader_token,
        "team_leader_user_id": team_leader_user_id,
        "team_leader_user_username": team_leader_user_username,
        "farm_worker_token": farm_worker_token,
        "farm_worker_user_id": farm_worker_user_id,
        "farm_worker_user_username": farm_worker_user_username,
    }


@pytest.fixture
def setup_cows():
    """
    Fixture to create a sample cows object for testing.
    """
    general_cow = {
        "name": "General Cow",
        "breed": {"name": CowBreedChoices.AYRSHIRE},
        "date_of_birth": todays_date - timedelta(days=370),
        "gender": SexChoices.FEMALE,
        "availability_status": CowAvailabilityChoices.ALIVE,
        "current_pregnancy_status": CowPregnancyChoices.OPEN,
        "category": CowCategoryChoices.HEIFER,
        "current_production_status": CowProductionStatusChoices.OPEN,
    }
    return general_cow


@pytest.fixture
def setup_inseminators_data():
    inseminators_data = {
        "first_name": "Peter",
        "last_name": "Evance",
        "phone_number": "+254712345678",
        "sex": SexChoices.MALE,
        "company": "Peter's Breeders",
        "license_number": "ABC-2023",
    }
    return inseminators_data


@pytest.fixture
@pytest.mark.django_db
def setup_insemination_data():
    inseminators_data = {
        "first_name": "Peter",
        "last_name": "Evance",
        "phone_number": "+254712345678",
        "sex": SexChoices.MALE,
        "company": "Peter's Breeders",
        "license_number": "ABC-2023",
    }
    serializer1 = InseminatorSerializer(data=inseminators_data)
    assert serializer1.is_valid()
    inseminator = serializer1.save()

    general_cow = {
        "name": "General Cow",
        "breed": {"name": CowBreedChoices.AYRSHIRE},
        "date_of_birth": todays_date - timedelta(days=366),
        "gender": SexChoices.FEMALE,
        "availability_status": CowAvailabilityChoices.ALIVE,
        "current_pregnancy_status": CowPregnancyChoices.OPEN,
        "category": CowCategoryChoices.HEIFER,
        "current_production_status": CowProductionStatusChoices.OPEN,
    }

    serializer2 = CowSerializer(data=general_cow)
    assert serializer2.is_valid()
    cow = serializer2.save()

    heat_data = {"observation_time": timezone.now(), "cow": cow.id}

    serializer3 = HeatSerializer(data=heat_data)
    assert serializer3.is_valid()
    serializer3.save()

    insemination_data = {
        "cow": cow.id,
        "inseminator": inseminator.id,
    }
    return insemination_data


@pytest.fixture
@pytest.mark.django_db
def setup_pregnancy_data():
    general_cow = {
        "name": "General Cow",
        "breed": {"name": CowBreedChoices.AYRSHIRE},
        "date_of_birth": todays_date - timedelta(days=650),
        "gender": SexChoices.FEMALE,
        "availability_status": CowAvailabilityChoices.ALIVE,
        "current_pregnancy_status": CowPregnancyChoices.OPEN,
        "category": CowCategoryChoices.HEIFER,
        "current_production_status": CowProductionStatusChoices.OPEN,
    }

    serializer = CowSerializer(data=general_cow)
    assert serializer.is_valid()
    cow = serializer.save()

    pregnancy_data = {"cow": cow.id, "start_date": todays_date - timedelta(days=270)}
    return pregnancy_data


@pytest.fixture
@pytest.mark.django_db
def setup_pregnancy_to_lactation_data():
    general_cow = {
        "name": "General Cow",
        "breed": {"name": CowBreedChoices.AYRSHIRE},
        "date_of_birth": todays_date - timedelta(days=735),
        "gender": SexChoices.FEMALE,
        "availability_status": CowAvailabilityChoices.ALIVE,
        "current_pregnancy_status": CowPregnancyChoices.OPEN,
        "category": CowCategoryChoices.HEIFER,
        "current_production_status": CowProductionStatusChoices.OPEN,
    }

    serializer = CowSerializer(data=general_cow)
    assert serializer.is_valid()
    cow = serializer.save()

    pregnancy_to_lactation_data = {
        "cow": cow.id,
        "start_date": todays_date - timedelta(days=370),
        "date_of_calving": todays_date - timedelta(days=100),
        "pregnancy_outcome": PregnancyOutcomeChoices.LIVE,
        "pregnancy_status": PregnancyStatusChoices.CONFIRMED,
    }
    return pregnancy_to_lactation_data


@pytest.fixture
@pytest.mark.django_db
def setup_weight_record_data():
    general_cow = {
        "name": "General Cow",
        "breed": {"name": CowBreedChoices.AYRSHIRE},
        "date_of_birth": todays_date - timedelta(days=650),
        "gender": SexChoices.FEMALE,
        "availability_status": CowAvailabilityChoices.ALIVE,
        "current_pregnancy_status": CowPregnancyChoices.OPEN,
        "category": CowCategoryChoices.HEIFER,
        "current_production_status": CowProductionStatusChoices.OPEN,
    }

    serializer = CowSerializer(data=general_cow)
    assert serializer.is_valid()
    cow = serializer.save()

    weight_data = {"cow": cow.id, "weight_in_kgs": 1150}
    return weight_data


@pytest.fixture
@pytest.mark.django_db
def setup_culling_record_data():
    general_cow = {
        "name": "General Cow",
        "breed": {"name": CowBreedChoices.AYRSHIRE},
        "date_of_birth": todays_date - timedelta(days=650),
        "gender": SexChoices.FEMALE,
        "availability_status": CowAvailabilityChoices.ALIVE,
        "current_pregnancy_status": CowPregnancyChoices.OPEN,
        "category": CowCategoryChoices.HEIFER,
        "current_production_status": CowProductionStatusChoices.OPEN,
    }

    serializer = CowSerializer(data=general_cow)
    assert serializer.is_valid()
    cow = serializer.save()

    culling_data = {
        "cow": cow.id,
        "reason": CullingReasonChoices.CONSISTENT_LOW_PRODUCTION,
    }
    return culling_data


@pytest.fixture
@pytest.mark.django_db
def setup_quarantine_record_data():
    general_cow = {
        "name": "General Cow",
        "breed": {"name": CowBreedChoices.AYRSHIRE},
        "date_of_birth": todays_date - timedelta(days=650),
        "gender": SexChoices.FEMALE,
        "availability_status": CowAvailabilityChoices.ALIVE,
        "current_pregnancy_status": CowPregnancyChoices.OPEN,
        "category": CowCategoryChoices.HEIFER,
        "current_production_status": CowProductionStatusChoices.OPEN,
    }

    serializer = CowSerializer(data=general_cow)
    assert serializer.is_valid()
    cow = serializer.save()

    quarantine_data = {
        "cow": cow.id,
        "reason": QuarantineReasonChoices.NEW_COW,
    }
    return quarantine_data


@pytest.fixture()
def setup_barn_data():
    barn_data = {
        "name": "BARN A",
        "capacity": 50
    }

    return {"barn_data": barn_data}


@pytest.fixture()
def setup_cow_pen_data():
    barn_data = {
        "name": "BARN A",
        "capacity": 20
    }

    serializer = BarnSerializer(data=barn_data)
    serializer.is_valid()
    barn = serializer.save()

    cow_pen_data = {
        "barn": barn.id,
        "pen_type": CowPenTypeChoices.FIXED,
        "category": CowPenCategoriesChoices.CALF_PEN,
        "capacity": 3
    }

    return {"cow_pen_data": cow_pen_data}


@pytest.fixture()
def setup_cow_in_pen_movement_data():
    barn_data = {
        "name": "BARN A",
        "capacity": 20
    }

    serializer1 = BarnSerializer(data=barn_data)
    serializer1.is_valid()
    barn = serializer1.save()

    cow_pen_1_data = {
        "barn": barn.id,
        "pen_type": CowPenTypeChoices.FIXED,
        "category": CowPenCategoriesChoices.CALF_PEN,
        "capacity": 1
    }
    serializer2 = CowPenSerializer(data=cow_pen_1_data)
    serializer2.is_valid()
    cow_pen_1 = serializer2.save()

    cow_pen_2_data = {
        "barn": barn.id,
        "pen_type": CowPenTypeChoices.FIXED,
        "category": CowPenCategoriesChoices.HEIFER_PEN,
        "capacity": 2
    }
    serializer3 = CowPenSerializer(data=cow_pen_2_data)
    serializer3.is_valid()
    cow_pen_2 = serializer3.save()

    cow = {
        "name": "General Cow",
        "breed": {"name": CowBreedChoices.AYRSHIRE},
        "date_of_birth": todays_date - timedelta(days=370),
        "gender": SexChoices.FEMALE,
        "availability_status": CowAvailabilityChoices.ALIVE,
        "current_pregnancy_status": CowPregnancyChoices.OPEN,
        "category": CowCategoryChoices.HEIFER,
        "current_production_status": CowProductionStatusChoices.OPEN,
    }

    serializer4 = CowSerializer(data=cow)
    serializer4.is_valid()
    cow = serializer4.save()

    cow_in_pen_movement_data = {
        "cow": cow.id,
        "previous_pen": cow_pen_2.id,
        "new_pen": cow_pen_1.id
    }

    return {"cow_in_pen_movement_data": cow_in_pen_movement_data,
            "cow_pen_2": cow_pen_2}
