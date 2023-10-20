import pytest
from django.urls import reverse
from rest_framework import status

from poultry_inventory.models import *


@pytest.mark.django_db
class TestFlockSourceViewSet:
    @pytest.fixture(autouse=True)
    def setup(self, setup_users):
        self.client = setup_users["client"]

        self.regular_user_token = setup_users["regular_user_token"]
        self.farm_owner_token = setup_users["farm_owner_token"]
        self.farm_manager_token = setup_users["farm_manager_token"]
        self.asst_farm_manager_token = setup_users["asst_farm_manager_token"]
        self.team_leader_token = setup_users["team_leader_token"]
        self.farm_worker_token = setup_users["farm_worker_token"]

    def test_create_flock_source_as_farm_owner(self):
        """
        Test creating a flock source by a farm owner.
        """
        flock_source_data = {"name": FlockSourceChoices.KEN_CHICK}
        response = self.client.post(
            reverse("poultry:flock-sources-list"),
            data=flock_source_data,
            HTTP_AUTHORIZATION=f"Token {self.farm_owner_token}",
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert FlockSource.objects.filter(name=flock_source_data["name"]).exists()

    def test_create_flock_source_as_farm_manager(self):
        """
        Test creating a flock source by a farm manager
        """
        flock_source_data = {"name": FlockSourceChoices.KEN_CHICK}
        response = self.client.post(
            reverse("poultry:flock-sources-list"),
            flock_source_data,
            HTTP_AUTHORIZATION=f"Token {self.farm_manager_token}",
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert FlockSource.objects.filter(name=flock_source_data["name"]).exists()

    def test_create_flock_source_as_asst_farm_manager_permission_denied(self):
        """
        Test creating a flock source by an assistant farm manager (should be denied).
        """
        flock_source_data = {"name": FlockSourceChoices.KEN_CHICK}
        response = self.client.post(
            reverse("poultry:flock-sources-list"),
            flock_source_data,
            HTTP_AUTHORIZATION=f"Token {self.asst_farm_manager_token}",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not FlockSource.objects.filter(
            name=flock_source_data["name"]
        ).exists()

    def test_create_flock_source_as_team_leader_permission_denied(self):
        """
        Test creating a flock source by a team leader (should be denied).
        """
        flock_source_data = {"name": FlockSourceChoices.KEN_CHICK}
        response = self.client.post(
            reverse("poultry:flock-sources-list"),
            flock_source_data,
            HTTP_AUTHORIZATION=f"Token {self.team_leader_token}",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not FlockSource.objects.filter(
            name=flock_source_data["name"]
        ).exists()

    def test_create_flock_source_as_farm_worker_permission_denied(self):
        """
        Test creating a flock source by a farm worker (should be denied).
        """
        flock_source_data = {"name": FlockSourceChoices.THIS_FARM}
        response = self.client.post(
            reverse("poultry:flock-sources-list"),
            flock_source_data,
            HTTP_AUTHORIZATION=f"Token {self.farm_worker_token}",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not FlockSource.objects.filter(
            name=flock_source_data["name"]
        ).exists()

    def test_create_flock_source_as_regular_user_permission_denied(self):
        """
        Test creating a flock source by a regular user (should be denied).
        """
        flock_source_data = {"name": FlockSourceChoices.THIS_FARM}
        response = self.client.post(
            reverse("poultry:flock-sources-list"),
            flock_source_data,
            HTTP_AUTHORIZATION=f"Token {self.regular_user_token}",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not FlockSource.objects.filter(
            name=flock_source_data["name"]
        ).exists()

    def test_create_flock_source_without_authentication(self):
        """
        Test creating a flock source without authentication (should be denied).
        """
        flock_source_data = {"name": FlockSourceChoices.THIS_FARM}
        response = self.client.post(
            reverse("poultry:flock-sources-list"), flock_source_data
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert not FlockSource.objects.filter(
            name=flock_source_data["name"]
        ).exists()

    def test_retrieve_flock_sources_as_farm_owner(self):
        """
        Test retrieving flock sources by a farm owner.
        """
        response = self.client.get(
            reverse("poultry:flock-sources-list"),
            HTTP_AUTHORIZATION=f"Token {self.farm_owner_token}",
        )
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_flock_sources_as_farm_manager(self):
        """
        Test retrieving flock sources by a farm manager.
        """
        response = self.client.get(
            reverse("poultry:flock-sources-list"),
            HTTP_AUTHORIZATION=f"Token {self.farm_manager_token}",
        )
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_flock_sources_as_asst_farm_manager(self):
        """
        Test retrieving flock sources by an assistant farm manager.
        """
        response = self.client.get(
            reverse("poultry:flock-sources-list"),
            HTTP_AUTHORIZATION=f"Token {self.asst_farm_manager_token}",
        )
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_flock_sources_as_team_leader(self):
        """
        Test retrieving flock sources by a team leader.
        """
        response = self.client.get(
            reverse("poultry:flock-sources-list"),
            HTTP_AUTHORIZATION=f"Token {self.team_leader_token}",
        )
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_flock_source_as_regular_user_permission_denied(self):
        """
        Test retrieving flock sources by a regular user (should be denied).
        """
        response = self.client.get(
            reverse("poultry:flock-sources-list"),
            HTTP_AUTHORIZATION=f"Token {self.regular_user_token}",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_retrieve_flock_source_without_authentication(self):
        """
        Test retrieving flock sources without authentication (should be denied).
        """
        url = reverse("poultry:flock-sources-list")
        response = self.client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_flock_source_permission_denied(self):
        """
        Test updating a flock source (should be denied).
        """
        flock_source = FlockSource.objects.create(name=FlockSourceChoices.THIS_FARM)
        url = reverse("poultry:flock-sources-detail", kwargs={"pk": flock_source.id})
        flock_source_update_data = {"name": FlockSourceChoices.THIS_FARM}
        response = self.client.put(
            url,
            flock_source_update_data,
            HTTP_AUTHORIZATION=f"Token {self.farm_owner_token}",
        )
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_delete_flock_source_as_farm_owner(self):
        """
        Test deleting a flock source by a farm owner.
        """
        flock_source = FlockSource.objects.create(name=FlockSourceChoices.THIS_FARM)
        url = reverse("poultry:flock-sources-detail", kwargs={"pk": flock_source.id})
        response = self.client.delete(
            url, HTTP_AUTHORIZATION=f"Token {self.farm_owner_token}"
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not FlockSource.objects.filter(id=flock_source.id).exists()

    def test_delete_flock_source_as_farm_manager(self):
        """
        Test deleting a flock source by a farm manager.
        """
        flock_source = FlockSource.objects.create(
            name=FlockSourceChoices.UZIMA_CHICKEN
        )
        url = reverse("poultry:flock-sources-detail", kwargs={"pk": flock_source.id})
        response = self.client.delete(
            url, HTTP_AUTHORIZATION=f"Token {self.farm_manager_token}"
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not FlockSource.objects.filter(id=flock_source.id).exists()

    def test_delete_flock_source_as_asst_farm_manager_permission_denied(self):
        """
        Test deleting a flock source by an assistant farm manager (should be denied).
        """
        flock_source = FlockSource.objects.create(name=FlockSourceChoices.THIS_FARM)
        url = reverse("poultry:flock-sources-detail", kwargs={"pk": flock_source.id})
        response = self.client.delete(
            url, HTTP_AUTHORIZATION=f"Token {self.asst_farm_manager_token}"
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert FlockSource.objects.filter(id=flock_source.id).exists()

    def test_delete_flock_source_as_team_leader_permission_denied(self):
        """
        Test deleting a flock source by a team leader (should be denied).
        """
        flock_source = FlockSource.objects.create(name=FlockSourceChoices.THIS_FARM)
        url = reverse("poultry:flock-sources-detail", kwargs={"pk": flock_source.id})
        response = self.client.delete(
            url, HTTP_AUTHORIZATION=f"Token {self.team_leader_token}"
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert FlockSource.objects.filter(id=flock_source.id).exists()

    def test_delete_flock_source_as_farm_worker_permission_denied(self):
        """
        Test deleting a flock source by a farm worker (should be denied).
        """
        flock_source = FlockSource.objects.create(name=FlockSourceChoices.THIS_FARM)
        url = reverse("poultry:flock-sources-detail", kwargs={"pk": flock_source.id})
        response = self.client.delete(
            url, HTTP_AUTHORIZATION=f"Token {self.farm_worker_token}"
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert FlockSource.objects.filter(id=flock_source.id).exists()

    def test_delete_flock_source_as_regular_user_permission_denied(self):
        """
        Test delete flock source as a regular user (permission denied)
        """
        flock_source = FlockSource.objects.create(
            name=FlockSourceChoices.UZIMA_CHICKEN
        )
        url = reverse("poultry:flock-sources-detail", kwargs={"pk": flock_source.id})

        response = self.client.delete(
            url, HTTP_AUTHORIZATION=f"Token {self.regular_user_token}"
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert FlockSource.objects.filter(id=flock_source.id).exists()

    def test_delete_flock_source_unauthorized(self):
        """
        Test delete flock source by unauthorized request
        """
        flock_source = FlockSource.objects.create(
            name=FlockSourceChoices.UZIMA_CHICKEN
        )
        url = reverse("poultry:flock-sources-detail", kwargs={"pk": flock_source.id})

        response = self.client.delete(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert FlockSource.objects.filter(id=flock_source.id).exists()

    def test_filter_flock_source_by_source(self):
        """
        Test filtering flock sources by source (e.g., get all breeds with source 'KIPLELS_FARM').
        """
        FlockSource.objects.create(name=FlockSourceChoices.KIPLELS_FARM)
        FlockSource.objects.create(name=FlockSourceChoices.THIS_FARM)
        url = reverse("poultry:flock-sources-list")
        url += f"?name={FlockSourceChoices.KIPLELS_FARM}"

        response = self.client.get(
            url, HTTP_AUTHORIZATION=f"Token {self.farm_owner_token}"
        )

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["name"] == FlockSourceChoices.KIPLELS_FARM

    def test_filter_flock_source_by_partial_source(self):
        """
        Test filtering flock sources by partial source (e.g., get breeds with sources containing 'ey').
        """
        FlockSource.objects.create(name=FlockSourceChoices.KIPLELS_FARM)
        FlockSource.objects.create(name=FlockSourceChoices.KEN_CHICK)
        url = reverse("poultry:flock-sources-list")
        url += "?name=ken"

        response = self.client.get(
            url, HTTP_AUTHORIZATION=f"Token {self.asst_farm_manager_token}"
        )
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_order_flock_source_by_multiple_fields(self):
        """
        Test ordering flock sources by multiple fields (e.g., source in descending order, id in ascending order).
        """
        FlockSource.objects.create(name=FlockSourceChoices.KIPLELS_FARM)
        FlockSource.objects.create(name=FlockSourceChoices.KEN_CHICK)
        FlockSource.objects.create(name=FlockSourceChoices.THIS_FARM)
        FlockSource.objects.create(name=FlockSourceChoices.UZIMA_CHICKEN)

        url = reverse("poultry:flock-sources-list")
        url += "?ordering=-name"

        response = self.client.get(
            url, HTTP_AUTHORIZATION=f"Token {self.farm_manager_token}"
        )
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 4
        assert response.data[0]["name"] == FlockSourceChoices.UZIMA_CHICKEN
        assert response.data[1]["name"] == FlockSourceChoices.THIS_FARM
        assert response.data[2]["name"] == FlockSourceChoices.KIPLELS_FARM
        assert response.data[3]["name"] == FlockSourceChoices.KEN_CHICK

    def test_no_results_for_invalid_source(self):
        """
        Test filtering with a source that doesn't exist.
        """
        url = reverse("poultry:flock-sources-list")
        url += "?name=nonexistent"
        response = self.client.get(
            url, HTTP_AUTHORIZATION=f"Token {self.farm_owner_token}"
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data == {
            "detail": "No flock source(s) found matching the provided filters."
        }


@pytest.mark.django_db
class TestFlockBreedViewSet:
    @pytest.fixture(autouse=True)
    def setup(self, setup_users):
        self.client = setup_users["client"]

        self.regular_user_token = setup_users["regular_user_token"]
        self.farm_owner_token = setup_users["farm_owner_token"]
        self.farm_manager_token = setup_users["farm_manager_token"]
        self.asst_farm_manager_token = setup_users["asst_farm_manager_token"]
        self.team_leader_token = setup_users["team_leader_token"]
        self.farm_worker_token = setup_users["farm_worker_token"]

    def test_create_flock_breed_as_farm_owner(self):
        """
        Test creating a flock breed by a farm owner.
        """
        flock_breed_data = {"name": FlockBreedTypeChoices.KENBRO}
        response = self.client.post(
            reverse("poultry:flock-breeds-list"),
            data=flock_breed_data,
            HTTP_AUTHORIZATION=f"Token {self.farm_owner_token}",
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert FlockBreed.objects.filter(name=flock_breed_data["name"]).exists()

    def test_create_flock_breed_as_farm_manager(self):
        """
        Test creating a flock breed by a farm manager
        """
        flock_breed_data = {"name": FlockBreedTypeChoices.KENBRO}
        response = self.client.post(
            reverse("poultry:flock-breeds-list"),
            flock_breed_data,
            HTTP_AUTHORIZATION=f"Token {self.farm_manager_token}",
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert FlockBreed.objects.filter(name=flock_breed_data["name"]).exists()

    def test_create_flock_breed_as_asst_farm_manager_permission_denied(self):
        """
        Test creating a flock breed by an assistant farm manager (should be denied).
        """
        flock_breed_data = {"name": FlockBreedTypeChoices.KENBRO}
        response = self.client.post(
            reverse("poultry:flock-breeds-list"),
            flock_breed_data,
            HTTP_AUTHORIZATION=f"Token {self.asst_farm_manager_token}",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not FlockBreed.objects.filter(name=flock_breed_data["name"]).exists()

    def test_create_flock_breed_as_team_leader_permission_denied(self):
        """
        Test creating a flock breed by a team leader (should be denied).
        """
        flock_breed_data = {"name": FlockBreedTypeChoices.KENBRO}
        response = self.client.post(
            reverse("poultry:flock-breeds-list"),
            flock_breed_data,
            HTTP_AUTHORIZATION=f"Token {self.team_leader_token}",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not FlockBreed.objects.filter(name=flock_breed_data["name"]).exists()

    def test_create_flock_breed_as_farm_worker_permission_denied(self):
        """
        Test creating a flock breed by a farm worker (should be denied).
        """
        flock_breed_data = {"breed": FlockBreedTypeChoices.BANTAM}
        response = self.client.post(
            reverse("poultry:flock-breeds-list"),
            flock_breed_data,
            HTTP_AUTHORIZATION=f"Token {self.farm_worker_token}",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not FlockBreed.objects.filter(name=flock_breed_data["breed"]).exists()

    def test_create_flock_breed_as_regular_user_permission_denied(self):
        """
        Test creating a flock breed by a regular user (should be denied).
        """
        flock_breed_data = {"breed": FlockBreedTypeChoices.RAINBOW_ROOSTER}
        response = self.client.post(
            reverse("poultry:flock-breeds-list"),
            flock_breed_data,
            HTTP_AUTHORIZATION=f"Token {self.regular_user_token}",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not FlockBreed.objects.filter(name=flock_breed_data["breed"]).exists()

    def test_create_flock_breed_without_authentication(self):
        """
        Test creating a flock breed without authentication (should be denied).
        """
        flock_breed_data = {"breed": FlockBreedTypeChoices.RAINBOW_ROOSTER}
        response = self.client.post(
            reverse("poultry:flock-breeds-list"), flock_breed_data
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert not FlockBreed.objects.filter(name=flock_breed_data["breed"]).exists()

    def test_retrieve_flock_breeds_as_farm_owner(self):
        """
        Test retrieving flock breeds by a farm owner.
        """
        response = self.client.get(
            reverse("poultry:flock-breeds-list"),
            HTTP_AUTHORIZATION=f"Token {self.farm_owner_token}",
        )
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_flock_breeds_as_farm_manager(self):
        """
        Test retrieving flock breeds by a farm manager.
        """
        response = self.client.get(
            reverse("poultry:flock-breeds-list"),
            HTTP_AUTHORIZATION=f"Token {self.farm_manager_token}",
        )
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_flock_breeds_as_asst_farm_manager(self):
        """
        Test retrieving flock breeds by an assistant farm manager.
        """
        response = self.client.get(
            reverse("poultry:flock-breeds-list"),
            HTTP_AUTHORIZATION=f"Token {self.asst_farm_manager_token}",
        )
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_flock_breeds_as_team_leader(self):
        """
        Test retrieving flock breeds by a team leader.
        """
        response = self.client.get(
            reverse("poultry:flock-breeds-list"),
            HTTP_AUTHORIZATION=f"Token {self.team_leader_token}",
        )
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_flock_breed_as_regular_user_permission_denied(self):
        """
        Test retrieving flock breeds by a regular user (should be denied).
        """
        response = self.client.get(
            reverse("poultry:flock-breeds-list"),
            HTTP_AUTHORIZATION=f"Token {self.regular_user_token}",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_retrieve_flock_breed_without_authentication(self):
        """
        Test retrieving flock breeds without authentication (should be denied).
        """
        url = reverse("poultry:flock-breeds-list")
        response = self.client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_flock_breed_permission_denied(self):
        """
        Test updating a flock breed (should be denied).
        """
        flock_breed = FlockBreed.objects.create(
            name=FlockBreedTypeChoices.RAINBOW_ROOSTER
        )
        url = reverse("poultry:flock-breeds-detail", kwargs={"pk": flock_breed.id})
        flock_breed_update_data = {"breed": FlockBreedTypeChoices.RAINBOW_ROOSTER}
        response = self.client.put(
            url,
            flock_breed_update_data,
            HTTP_AUTHORIZATION=f"Token {self.farm_owner_token}",
        )
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_delete_flock_breed_as_farm_owner(self):
        """
        Test deleting a flock breed by a farm owner.
        """
        flock_breed = FlockBreed.objects.create(
            name=FlockBreedTypeChoices.RAINBOW_ROOSTER
        )
        url = reverse("poultry:flock-breeds-detail", kwargs={"pk": flock_breed.id})
        response = self.client.delete(
            url, HTTP_AUTHORIZATION=f"Token {self.farm_owner_token}"
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not FlockBreed.objects.filter(id=flock_breed.id).exists()

    def test_delete_flock_breed_as_farm_manager(self):
        """
        Test deleting a flock breed by a farm manager.
        """
        flock_breed = FlockBreed.objects.create(
            name=FlockBreedTypeChoices.RAINBOW_ROOSTER
        )
        url = reverse("poultry:flock-breeds-detail", kwargs={"pk": flock_breed.id})
        response = self.client.delete(
            url, HTTP_AUTHORIZATION=f"Token {self.farm_manager_token}"
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not FlockBreed.objects.filter(id=flock_breed.id).exists()

    def test_delete_flock_breed_as_asst_farm_manager_permission_denied(self):
        """
        Test deleting a flock breed by an assistant farm manager (should be denied).
        """
        flock_breed = FlockBreed.objects.create(
            name=FlockBreedTypeChoices.RAINBOW_ROOSTER
        )
        url = reverse("poultry:flock-breeds-detail", kwargs={"pk": flock_breed.id})
        response = self.client.delete(
            url, HTTP_AUTHORIZATION=f"Token {self.asst_farm_manager_token}"
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert FlockBreed.objects.filter(id=flock_breed.id).exists()

    def test_delete_flock_breed_as_team_leader_permission_denied(self):
        """
        Test deleting a flock breed by a team leader (should be denied).
        """
        flock_breed = FlockBreed.objects.create(
            name=FlockBreedTypeChoices.RAINBOW_ROOSTER
        )
        url = reverse("poultry:flock-breeds-detail", kwargs={"pk": flock_breed.id})
        response = self.client.delete(
            url, HTTP_AUTHORIZATION=f"Token {self.team_leader_token}"
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert FlockBreed.objects.filter(id=flock_breed.id).exists()

    def test_delete_flock_breed_as_farm_worker_permission_denied(self):
        """
        Test deleting a flock breed by a farm worker (should be denied).
        """
        flock_breed = FlockBreed.objects.create(
            name=FlockBreedTypeChoices.RAINBOW_ROOSTER
        )
        url = reverse("poultry:flock-breeds-detail", kwargs={"pk": flock_breed.id})
        response = self.client.delete(
            url, HTTP_AUTHORIZATION=f"Token {self.farm_worker_token}"
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert FlockBreed.objects.filter(id=flock_breed.id).exists()

    def test_delete_flock_breed_as_regular_user_permission_denied(self):
        """
        Test delete flock breed as a regular user (permission denied)
        """
        flock_breed = FlockBreed.objects.create(
            name=FlockBreedTypeChoices.RAINBOW_ROOSTER
        )
        url = reverse("poultry:flock-breeds-detail", kwargs={"pk": flock_breed.id})

        response = self.client.delete(
            url, HTTP_AUTHORIZATION=f"Token {self.regular_user_token}"
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert FlockBreed.objects.filter(id=flock_breed.id).exists()

    def test_delete_flock_breed_unauthorized(self):
        """
        Test delete flock breed by unauthorized request
        """
        flock_breed = FlockBreed.objects.create(
            name=FlockBreedTypeChoices.RAINBOW_ROOSTER
        )
        url = reverse("poultry:flock-breeds-detail", kwargs={"pk": flock_breed.id})

        response = self.client.delete(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert FlockBreed.objects.filter(id=flock_breed.id).exists()

    def test_filter_flock_breed_by_breed(self):
        """
        Test filtering flock breeds by breed (e.g., get all breeds with breed 'KIPLELS_FARM').
        """
        FlockBreed.objects.create(name=FlockBreedTypeChoices.BRAHMA)
        FlockBreed.objects.create(name=FlockBreedTypeChoices.INDIGENOUS)
        url = reverse("poultry:flock-breeds-list")
        url += f"?name={FlockBreedTypeChoices.INDIGENOUS}"

        response = self.client.get(
            url, HTTP_AUTHORIZATION=f"Token {self.farm_owner_token}"
        )

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["name"] == FlockBreedTypeChoices.INDIGENOUS

    def test_filter_flock_breed_by_partial_breed(self):
        """
        Test filtering flock breeds by partial breed (e.g., get breeds with breeds containing 'ey').
        """
        FlockBreed.objects.create(name=FlockBreedTypeChoices.COCHIN)
        FlockBreed.objects.create(name=FlockBreedTypeChoices.LEGHORN)
        url = reverse("poultry:flock-breeds-list")
        url += "?name=leg"

        response = self.client.get(
            url, HTTP_AUTHORIZATION=f"Token {self.asst_farm_manager_token}"
        )
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_order_flock_breed_by_multiple_fields(self):
        """
        Test ordering flock breeds by multiple fields (e.g., breed in descending order, id in ascending order).
        """
        FlockBreed.objects.create(name=FlockBreedTypeChoices.RAINBOW_ROOSTER)
        FlockBreed.objects.create(name=FlockBreedTypeChoices.EASTER_EGGER)
        FlockBreed.objects.create(name=FlockBreedTypeChoices.INDIGENOUS)
        FlockBreed.objects.create(name=FlockBreedTypeChoices.LEGHORN)

        url = reverse("poultry:flock-breeds-list")
        url += "?ordering=-name"

        response = self.client.get(
            url, HTTP_AUTHORIZATION=f"Token {self.farm_manager_token}"
        )
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 4
        assert response.data[0]["name"] == FlockBreedTypeChoices.RAINBOW_ROOSTER
        assert response.data[1]["name"] == FlockBreedTypeChoices.LEGHORN
        assert response.data[2]["name"] == FlockBreedTypeChoices.INDIGENOUS
        assert response.data[3]["name"] == FlockBreedTypeChoices.EASTER_EGGER

    def test_no_results_for_invalid_breed(self):
        """
        Test filtering with a breed that doesn't exist.
        """
        url = reverse("poultry:flock-breeds-list")
        url += "?name=nonexistent"
        response = self.client.get(
            url, HTTP_AUTHORIZATION=f"Token {self.farm_worker_token}"
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data == {
            "detail": "No flock breed(s) found matching the provided filters."
        }
