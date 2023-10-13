import pytest
from django.urls import reverse
from rest_framework import status

from users.models import *


@pytest.mark.django_db
def test_user_flow(client):
    # Register a new user
    register_data = {
        "username": "test@example.com",
        "password": "testpassword",
        "first_name": "Peter",
        "last_name": "Evance",
        "phone_number": "+254712345697",
        "sex": SexChoices.MALE,
    }

    response = client.post("/auth/users/", register_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert "username" in response.data
    user_id = response.data["id"]

    # Access user details (without authentication)
    response = client.get("/auth/users/me", follow=True)
    assert response.data["detail"] == "Authentication credentials were not provided."
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Log in
    login_data = {
        "username": "test@example.com",
        "password": "testpassword",
    }
    response = client.post(reverse("users:login"), login_data)
    assert response.status_code == status.HTTP_200_OK
    assert "auth_token" in response.data
    token = response.data["auth_token"]

    # Access user details (with authentication)
    headers = {"Authorization": f"Token {token}"}
    response = client.get(
        "/auth/users/me", HTTP_AUTHORIZATION=f"Token {token}", follow=True
    )
    assert response.status_code == status.HTTP_200_OK
    assert "username" in response.data
    assert response.data["username"] == "test@example.com"

    # Log out
    response = client.post(
        reverse("users:logout"),
        data={"token": token},
        HTTP_AUTHORIZATION=f"Token {token}",
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Attempt to access user details after logout
    headers = {"Authorization": f"Token {token}"}
    response = client.get(
        "/auth/users/me", HTTP_AUTHORIZATION=f"Token {token}", follow=True
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "detail" in response.data
    assert response.data["detail"] == "Invalid token."


@pytest.mark.django_db
class TestRoleAssignments:
    @pytest.fixture(autouse=True)
    def setup(self, setup_users):
        self.client = setup_users["client"]

        self.regular_user_id = setup_users["regular_user_id"]
        self.regular_user_token = setup_users["regular_user_token"]
        self.regular_user_username = setup_users["regular_user_username"]

        self.farm_owner_token = setup_users["farm_owner_token"]
        self.farm_owner_user_id = setup_users["farm_owner_user_id"]
        self.farm_owner_user_username = setup_users["farm_owner_user_username"]

        self.farm_manager_token = setup_users["farm_manager_token"]
        self.farm_manager_user_id = setup_users["farm_manager_user_id"]
        self.farm_manager_user_username = setup_users["farm_manager_user_username"]

        self.asst_farm_manager_token = setup_users["asst_farm_manager_token"]
        self.asst_farm_manager_user_id = setup_users["asst_farm_manager_user_id"]
        self.asst_farm_manager_user_username = setup_users[
            "asst_farm_manager_user_username"
        ]

        self.team_leader_token = setup_users["team_leader_token"]
        self.team_leader_user_id = setup_users["team_leader_user_id"]
        self.team_leader_user_username = setup_users["team_leader_user_username"]

        self.farm_worker_token = setup_users["farm_worker_token"]
        self.farm_worker_user_id = setup_users["farm_worker_user_id"]
        self.farm_worker_user_username = setup_users["farm_worker_user_username"]

    def test_assign_to_self(self):
        # Assigning the role to oneself should be restricted
        user_ids = [self.farm_owner_user_id]
        response = self.client.post(
            reverse("users:assign-farm-manager"),
            {"user_ids": user_ids},
            HTTP_AUTHORIZATION=f"Token {self.farm_owner_token}",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data[0] == "Cannot assign roles to yourself."

    def test_assign_farm_owner(self):
        user_ids = [self.regular_user_id]
        response = self.client.post(
            reverse("users:assign-farm-owner"),
            {"user_ids": user_ids},
            HTTP_AUTHORIZATION=f"Token {self.farm_owner_token}",
        )
        assert response.status_code == status.HTTP_200_OK
        assert (
            response.data["message"]
            == f"User {self.regular_user_username} has been assigned as a farm owner."
        )

    def test_assign_farm_manager(self):
        user_ids = [self.regular_user_id]
        response = self.client.post(
            reverse("users:assign-farm-manager"),
            {"user_ids": user_ids},
            HTTP_AUTHORIZATION=f"Token {self.farm_owner_token}",
        )
        assert response.status_code == status.HTTP_200_OK
        assert (
            response.data["message"]
            == f"User {self.regular_user_username} has been assigned as a farm manager."
        )

    def test_assign_asst_farm_manager(self):
        user_ids = [self.team_leader_user_id]
        response = self.client.post(
            reverse("users:assign-assistant-farm-manager"),
            {"user_ids": user_ids},
            HTTP_AUTHORIZATION=f"Token {self.farm_owner_token}",
        )
        assert response.status_code == status.HTTP_200_OK
        assert (
            response.data["message"]
            == f"User {self.team_leader_user_username} has been assigned as an assistant farm manager."
        )

    def test_assign_team_leader(self):
        user_ids = [self.regular_user_id]
        response = self.client.post(
            reverse("users:assign-team-leader"),
            {"user_ids": user_ids},
            HTTP_AUTHORIZATION=f"Token {self.asst_farm_manager_token}",
        )
        assert response.status_code == status.HTTP_200_OK
        assert (
            response.data["message"]
            == f"User {self.regular_user_username} has been assigned as a team leader."
        )

    def test_assign_farm_worker(self):
        user_ids = [self.regular_user_id]
        response = self.client.post(
            reverse("users:assign-farm-worker"),
            {"user_ids": user_ids},
            HTTP_AUTHORIZATION=f"Token {self.farm_manager_token}",
        )
        assert response.status_code == status.HTTP_200_OK
        assert (
            response.data["message"]
            == f"User {self.regular_user_username} has been assigned as a farm worker."
        )

    def test_assign_farm_manager_permission_denied(self):
        user_ids = [self.regular_user_id]
        response = self.client.post(
            reverse("users:assign-farm-manager"),
            {"user_ids": user_ids},
            HTTP_AUTHORIZATION=f"Token {self.farm_manager_token}",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert (
            response.data["message"]
            == "Only farm owners have permission to perform this action."
        )

    def test_assign_assistant_farm_manager_permission_denied(self):
        user_ids = [self.regular_user_id]

        response = self.client.post(
            reverse("users:assign-assistant-farm-manager"),
            {"user_ids": user_ids},
            HTTP_AUTHORIZATION=f"Token {self.farm_manager_token}",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert (
            response.data["message"]
            == "Only farm owners have permission to perform this action."
        )

    def test_assign_team_leader_permission_denied(self):
        user_ids = [self.regular_user_id]
        response = self.client.post(
            reverse("users:assign-team-leader"),
            {"user_ids": user_ids},
            HTTP_AUTHORIZATION=f"Token {self.farm_worker_token}",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert (
            response.data["message"]
            == "Only farm owners, managers, and assistants have permission to perform "
            "this action."
        )

    def test_assign_farm_worker_permission_denied(self):
        user_ids = [self.regular_user_id]
        response = self.client.post(
            reverse("users:assign-farm-worker"),
            {"user_ids": user_ids},
            HTTP_AUTHORIZATION=f"Token {self.asst_farm_manager_token}",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert (
            response.data["message"]
            == "Only farm owners and managers have permission to perform this action."
        )

    def test_dismiss_farm_manager(self):
        user_ids = [self.regular_user_id]
        response = self.client.post(
            reverse("users:dismiss-farm-manager"),
            {"user_ids": user_ids},
            HTTP_AUTHORIZATION=f"Token {self.farm_owner_token}",
        )
        assert response.status_code == status.HTTP_200_OK
        assert (
            response.data["message"]
            == f"User {self.regular_user_username} has been dismissed as a farm manager."
        )

    def test_dismiss_asst_farm_manager(self):
        user_ids = [self.farm_manager_user_id]
        response = self.client.post(
            reverse("users:dismiss-assistant-farm-manager"),
            {"user_ids": user_ids},
            HTTP_AUTHORIZATION=f"Token {self.farm_owner_token}",
        )
        assert response.status_code == status.HTTP_200_OK
        assert (
            response.data["message"]
            == f"User {self.farm_manager_user_username} has been dismissed as an "
            f"assistant farm manager."
        )

    def test_dismiss_team_leader(self):
        user_ids = [self.regular_user_id]
        response = self.client.post(
            reverse("users:dismiss-team-leader"),
            {"user_ids": user_ids},
            HTTP_AUTHORIZATION=f"Token {self.asst_farm_manager_token}",
        )
        assert response.status_code == status.HTTP_200_OK
        assert (
            response.data["message"]
            == f"User {self.regular_user_username} has been dismissed as a team leader."
        )

    def test_dismiss_farm_worker(self):
        user_ids = [self.regular_user_id]
        response = self.client.post(
            reverse("users:dismiss-farm-worker"),
            {"user_ids": user_ids},
            HTTP_AUTHORIZATION=f"Token {self.farm_manager_token}",
        )
        assert response.status_code == status.HTTP_200_OK
        assert (
            response.data["message"]
            == f"User {self.regular_user_username} has been dismissed as a farm worker."
        )

    def test_dismiss_user_not_found(self):
        user_ids = ["99"]
        response = self.client.post(
            reverse("users:dismiss-farm-manager"),
            {"user_ids": user_ids},
            HTTP_AUTHORIZATION=f"Token {self.farm_owner_token}",
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["error"] == "User with ID '99' was not found."
