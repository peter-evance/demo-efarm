import pytest
from django.urls import reverse
from rest_framework import status

from poultry.serializers import *
from poultry_inventory.models import *


# @pytest.mark.django_db
# class TestFlockSourceViewSet:
#     @pytest.fixture(autouse=True)
#     def setup(self, setup_users):
#         self.client = setup_users["client"]
#
#         self.regular_user_token = setup_users["regular_user_token"]
#         self.farm_owner_token = setup_users["farm_owner_token"]
#         self.farm_manager_token = setup_users["farm_manager_token"]
#         self.asst_farm_manager_token = setup_users["asst_farm_manager_token"]
#         self.team_leader_token = setup_users["team_leader_token"]
#         self.farm_worker_token = setup_users["farm_worker_token"]
#
#     def test_create_flock_source_as_farm_owner(self):
#         """
#         Test creating a flock source by a farm owner.
#         """
#         flock_source_data = {"name": FlockSourceChoices.KEN_CHICK}
#         response = self.client.post(
#             reverse("poultry:flock-sources-list"),
#             data=flock_source_data,
#             HTTP_AUTHORIZATION=f"Token {self.farm_owner_token}",
#         )
#         assert response.status_code == status.HTTP_201_CREATED
#         assert FlockSource.objects.filter(name=flock_source_data["name"]).exists()
#
#     def test_create_flock_source_as_farm_manager(self):
#         """
#         Test creating a flock source by a farm manager
#         """
#         flock_source_data = {"name": FlockSourceChoices.KEN_CHICK}
#         response = self.client.post(
#             reverse("poultry:flock-sources-list"),
#             flock_source_data,
#             HTTP_AUTHORIZATION=f"Token {self.farm_manager_token}",
#         )
#         assert response.status_code == status.HTTP_201_CREATED
#         assert FlockSource.objects.filter(name=flock_source_data["name"]).exists()
#
#     def test_create_flock_source_as_asst_farm_manager_permission_denied(self):
#         """
#         Test creating a flock source by an assistant farm manager (should be denied).
#         """
#         flock_source_data = {"name": FlockSourceChoices.KEN_CHICK}
#         response = self.client.post(
#             reverse("poultry:flock-sources-list"),
#             flock_source_data,
#             HTTP_AUTHORIZATION=f"Token {self.asst_farm_manager_token}",
#         )
#         assert response.status_code == status.HTTP_403_FORBIDDEN
#         assert not FlockSource.objects.filter(name=flock_source_data["name"]).exists()
#
#     def test_create_flock_source_as_team_leader_permission_denied(self):
#         """
#         Test creating a flock source by a team leader (should be denied).
#         """
#         flock_source_data = {"name": FlockSourceChoices.KEN_CHICK}
#         response = self.client.post(
#             reverse("poultry:flock-sources-list"),
#             flock_source_data,
#             HTTP_AUTHORIZATION=f"Token {self.team_leader_token}",
#         )
#         assert response.status_code == status.HTTP_403_FORBIDDEN
#         assert not FlockSource.objects.filter(name=flock_source_data["name"]).exists()
#
#     def test_create_flock_source_as_farm_worker_permission_denied(self):
#         """
#         Test creating a flock source by a farm worker (should be denied).
#         """
#         flock_source_data = {"name": FlockSourceChoices.THIS_FARM}
#         response = self.client.post(
#             reverse("poultry:flock-sources-list"),
#             flock_source_data,
#             HTTP_AUTHORIZATION=f"Token {self.farm_worker_token}",
#         )
#         assert response.status_code == status.HTTP_403_FORBIDDEN
#         assert not FlockSource.objects.filter(name=flock_source_data["name"]).exists()
#
#     def test_create_flock_source_as_regular_user_permission_denied(self):
#         """
#         Test creating a flock source by a regular user (should be denied).
#         """
#         flock_source_data = {"name": FlockSourceChoices.THIS_FARM}
#         response = self.client.post(
#             reverse("poultry:flock-sources-list"),
#             flock_source_data,
#             HTTP_AUTHORIZATION=f"Token {self.regular_user_token}",
#         )
#         assert response.status_code == status.HTTP_403_FORBIDDEN
#         assert not FlockSource.objects.filter(name=flock_source_data["name"]).exists()
#
#     def test_create_flock_source_without_authentication(self):
#         """
#         Test creating a flock source without authentication (should be denied).
#         """
#         flock_source_data = {"name": FlockSourceChoices.THIS_FARM}
#         response = self.client.post(
#             reverse("poultry:flock-sources-list"), flock_source_data
#         )
#         assert response.status_code == status.HTTP_401_UNAUTHORIZED
#         assert not FlockSource.objects.filter(name=flock_source_data["name"]).exists()
#
#     def test_retrieve_flock_sources_as_farm_owner(self):
#         """
#         Test retrieving flock sources by a farm owner.
#         """
#         response = self.client.get(
#             reverse("poultry:flock-sources-list"),
#             HTTP_AUTHORIZATION=f"Token {self.farm_owner_token}",
#         )
#         assert response.status_code == status.HTTP_200_OK
#
#     def test_retrieve_flock_sources_as_farm_manager(self):
#         """
#         Test retrieving flock sources by a farm manager.
#         """
#         response = self.client.get(
#             reverse("poultry:flock-sources-list"),
#             HTTP_AUTHORIZATION=f"Token {self.farm_manager_token}",
#         )
#         assert response.status_code == status.HTTP_200_OK
#
#     def test_retrieve_flock_sources_as_asst_farm_manager(self):
#         """
#         Test retrieving flock sources by an assistant farm manager.
#         """
#         response = self.client.get(
#             reverse("poultry:flock-sources-list"),
#             HTTP_AUTHORIZATION=f"Token {self.asst_farm_manager_token}",
#         )
#         assert response.status_code == status.HTTP_200_OK
#
#     def test_retrieve_flock_sources_as_team_leader(self):
#         """
#         Test retrieving flock sources by a team leader.
#         """
#         response = self.client.get(
#             reverse("poultry:flock-sources-list"),
#             HTTP_AUTHORIZATION=f"Token {self.team_leader_token}",
#         )
#         assert response.status_code == status.HTTP_200_OK
#
#     def test_retrieve_flock_source_as_regular_user_permission_denied(self):
#         """
#         Test retrieving flock sources by a regular user (should be denied).
#         """
#         response = self.client.get(
#             reverse("poultry:flock-sources-list"),
#             HTTP_AUTHORIZATION=f"Token {self.regular_user_token}",
#         )
#         assert response.status_code == status.HTTP_403_FORBIDDEN
#
#     def test_retrieve_flock_source_without_authentication(self):
#         """
#         Test retrieving flock sources without authentication (should be denied).
#         """
#         url = reverse("poultry:flock-sources-list")
#         response = self.client.get(url)
#         assert response.status_code == status.HTTP_401_UNAUTHORIZED
#
#     def test_update_flock_source_permission_denied(self):
#         """
#         Test updating a flock source (should be denied).
#         """
#         flock_source = FlockSource.objects.create(name=FlockSourceChoices.THIS_FARM)
#         url = reverse("poultry:flock-sources-detail", kwargs={"pk": flock_source.id})
#         flock_source_update_data = {"name": FlockSourceChoices.THIS_FARM}
#         response = self.client.put(
#             url,
#             flock_source_update_data,
#             HTTP_AUTHORIZATION=f"Token {self.farm_owner_token}",
#         )
#         assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
#
#     def test_delete_flock_source_as_farm_owner(self):
#         """
#         Test deleting a flock source by a farm owner.
#         """
#         flock_source = FlockSource.objects.create(name=FlockSourceChoices.THIS_FARM)
#         url = reverse("poultry:flock-sources-detail", kwargs={"pk": flock_source.id})
#         response = self.client.delete(
#             url, HTTP_AUTHORIZATION=f"Token {self.farm_owner_token}"
#         )
#         assert response.status_code == status.HTTP_204_NO_CONTENT
#         assert not FlockSource.objects.filter(id=flock_source.id).exists()
#
#     def test_delete_flock_source_as_farm_manager(self):
#         """
#         Test deleting a flock source by a farm manager.
#         """
#         flock_source = FlockSource.objects.create(name=FlockSourceChoices.UZIMA_CHICKEN)
#         url = reverse("poultry:flock-sources-detail", kwargs={"pk": flock_source.id})
#         response = self.client.delete(
#             url, HTTP_AUTHORIZATION=f"Token {self.farm_manager_token}"
#         )
#         assert response.status_code == status.HTTP_204_NO_CONTENT
#         assert not FlockSource.objects.filter(id=flock_source.id).exists()
#
#     def test_delete_flock_source_as_asst_farm_manager_permission_denied(self):
#         """
#         Test deleting a flock source by an assistant farm manager (should be denied).
#         """
#         flock_source = FlockSource.objects.create(name=FlockSourceChoices.THIS_FARM)
#         url = reverse("poultry:flock-sources-detail", kwargs={"pk": flock_source.id})
#         response = self.client.delete(
#             url, HTTP_AUTHORIZATION=f"Token {self.asst_farm_manager_token}"
#         )
#         assert response.status_code == status.HTTP_403_FORBIDDEN
#         assert FlockSource.objects.filter(id=flock_source.id).exists()
#
#     def test_delete_flock_source_as_team_leader_permission_denied(self):
#         """
#         Test deleting a flock source by a team leader (should be denied).
#         """
#         flock_source = FlockSource.objects.create(name=FlockSourceChoices.THIS_FARM)
#         url = reverse("poultry:flock-sources-detail", kwargs={"pk": flock_source.id})
#         response = self.client.delete(
#             url, HTTP_AUTHORIZATION=f"Token {self.team_leader_token}"
#         )
#         assert response.status_code == status.HTTP_403_FORBIDDEN
#         assert FlockSource.objects.filter(id=flock_source.id).exists()
#
#     def test_delete_flock_source_as_farm_worker_permission_denied(self):
#         """
#         Test deleting a flock source by a farm worker (should be denied).
#         """
#         flock_source = FlockSource.objects.create(name=FlockSourceChoices.THIS_FARM)
#         url = reverse("poultry:flock-sources-detail", kwargs={"pk": flock_source.id})
#         response = self.client.delete(
#             url, HTTP_AUTHORIZATION=f"Token {self.farm_worker_token}"
#         )
#         assert response.status_code == status.HTTP_403_FORBIDDEN
#         assert FlockSource.objects.filter(id=flock_source.id).exists()
#
#     def test_delete_flock_source_as_regular_user_permission_denied(self):
#         """
#         Test delete flock source as a regular user (permission denied)
#         """
#         flock_source = FlockSource.objects.create(name=FlockSourceChoices.UZIMA_CHICKEN)
#         url = reverse("poultry:flock-sources-detail", kwargs={"pk": flock_source.id})
#
#         response = self.client.delete(
#             url, HTTP_AUTHORIZATION=f"Token {self.regular_user_token}"
#         )
#         assert response.status_code == status.HTTP_403_FORBIDDEN
#         assert FlockSource.objects.filter(id=flock_source.id).exists()
#
#     def test_delete_flock_source_unauthorized(self):
#         """
#         Test delete flock source by unauthorized request
#         """
#         flock_source = FlockSource.objects.create(name=FlockSourceChoices.UZIMA_CHICKEN)
#         url = reverse("poultry:flock-sources-detail", kwargs={"pk": flock_source.id})
#
#         response = self.client.delete(url)
#         assert response.status_code == status.HTTP_401_UNAUTHORIZED
#         assert FlockSource.objects.filter(id=flock_source.id).exists()
#
#     def test_filter_flock_source_by_source(self):
#         """
#         Test filtering flock sources by source (e.g., get all breeds with source 'KIPLELS_FARM').
#         """
#         FlockSource.objects.create(name=FlockSourceChoices.KIPLELS_FARM)
#         FlockSource.objects.create(name=FlockSourceChoices.THIS_FARM)
#         url = reverse("poultry:flock-sources-list")
#         url += f"?name={FlockSourceChoices.KIPLELS_FARM}"
#
#         response = self.client.get(
#             url, HTTP_AUTHORIZATION=f"Token {self.farm_owner_token}"
#         )
#
#         assert response.status_code == status.HTTP_200_OK
#         assert len(response.data) == 1
#         assert response.data[0]["name"] == FlockSourceChoices.KIPLELS_FARM
#
#     def test_filter_flock_source_by_partial_source(self):
#         """
#         Test filtering flock sources by partial source (e.g., get breeds with sources containing 'ey').
#         """
#         FlockSource.objects.create(name=FlockSourceChoices.KIPLELS_FARM)
#         FlockSource.objects.create(name=FlockSourceChoices.KEN_CHICK)
#         url = reverse("poultry:flock-sources-list")
#         url += "?name=ken"
#
#         response = self.client.get(
#             url, HTTP_AUTHORIZATION=f"Token {self.asst_farm_manager_token}"
#         )
#         assert response.status_code == status.HTTP_200_OK
#         assert len(response.data) == 1
#
#     def test_order_flock_source_by_multiple_fields(self):
#         """
#         Test ordering flock sources by multiple fields (e.g., source in descending order, id in ascending order).
#         """
#         FlockSource.objects.create(name=FlockSourceChoices.KIPLELS_FARM)
#         FlockSource.objects.create(name=FlockSourceChoices.KEN_CHICK)
#         FlockSource.objects.create(name=FlockSourceChoices.THIS_FARM)
#         FlockSource.objects.create(name=FlockSourceChoices.UZIMA_CHICKEN)
#
#         url = reverse("poultry:flock-sources-list")
#         url += "?ordering=-name"
#
#         response = self.client.get(
#             url, HTTP_AUTHORIZATION=f"Token {self.farm_manager_token}"
#         )
#         assert response.status_code == status.HTTP_200_OK
#         assert len(response.data) == 4
#         assert response.data[0]["name"] == FlockSourceChoices.UZIMA_CHICKEN
#         assert response.data[1]["name"] == FlockSourceChoices.THIS_FARM
#         assert response.data[2]["name"] == FlockSourceChoices.KIPLELS_FARM
#         assert response.data[3]["name"] == FlockSourceChoices.KEN_CHICK
#
#     def test_no_results_for_invalid_source(self):
#         """
#         Test filtering with a source that doesn't exist.
#         """
#         url = reverse("poultry:flock-sources-list")
#         url += "?name=nonexistent"
#         response = self.client.get(
#             url, HTTP_AUTHORIZATION=f"Token {self.farm_owner_token}"
#         )
#         assert response.status_code == status.HTTP_404_NOT_FOUND
#         assert response.data == {
#             "detail": "No flock source(s) found matching the provided filters."
#         }
#
#
# @pytest.mark.django_db
# class TestFlockBreedViewSet:
#     @pytest.fixture(autouse=True)
#     def setup(self, setup_users):
#         self.client = setup_users["client"]
#
#         self.regular_user_token = setup_users["regular_user_token"]
#         self.farm_owner_token = setup_users["farm_owner_token"]
#         self.farm_manager_token = setup_users["farm_manager_token"]
#         self.asst_farm_manager_token = setup_users["asst_farm_manager_token"]
#         self.team_leader_token = setup_users["team_leader_token"]
#         self.farm_worker_token = setup_users["farm_worker_token"]
#
#     def test_create_flock_breed_as_farm_owner(self):
#         """
#         Test creating a flock breed by a farm owner.
#         """
#         flock_breed_data = {"name": FlockBreedTypeChoices.KENBRO}
#         response = self.client.post(
#             reverse("poultry:flock-breeds-list"),
#             data=flock_breed_data,
#             HTTP_AUTHORIZATION=f"Token {self.farm_owner_token}",
#         )
#         assert response.status_code == status.HTTP_201_CREATED
#         assert FlockBreed.objects.filter(name=flock_breed_data["name"]).exists()
#
#     def test_create_flock_breed_as_farm_manager(self):
#         """
#         Test creating a flock breed by a farm manager
#         """
#         flock_breed_data = {"name": FlockBreedTypeChoices.KENBRO}
#         response = self.client.post(
#             reverse("poultry:flock-breeds-list"),
#             flock_breed_data,
#             HTTP_AUTHORIZATION=f"Token {self.farm_manager_token}",
#         )
#         assert response.status_code == status.HTTP_201_CREATED
#         assert FlockBreed.objects.filter(name=flock_breed_data["name"]).exists()
#
#     def test_create_flock_breed_as_asst_farm_manager_permission_denied(self):
#         """
#         Test creating a flock breed by an assistant farm manager (should be denied).
#         """
#         flock_breed_data = {"name": FlockBreedTypeChoices.KENBRO}
#         response = self.client.post(
#             reverse("poultry:flock-breeds-list"),
#             flock_breed_data,
#             HTTP_AUTHORIZATION=f"Token {self.asst_farm_manager_token}",
#         )
#         assert response.status_code == status.HTTP_403_FORBIDDEN
#         assert not FlockBreed.objects.filter(name=flock_breed_data["name"]).exists()
#
#     def test_create_flock_breed_as_team_leader_permission_denied(self):
#         """
#         Test creating a flock breed by a team leader (should be denied).
#         """
#         flock_breed_data = {"name": FlockBreedTypeChoices.KENBRO}
#         response = self.client.post(
#             reverse("poultry:flock-breeds-list"),
#             flock_breed_data,
#             HTTP_AUTHORIZATION=f"Token {self.team_leader_token}",
#         )
#         assert response.status_code == status.HTTP_403_FORBIDDEN
#         assert not FlockBreed.objects.filter(name=flock_breed_data["name"]).exists()
#
#     def test_create_flock_breed_as_farm_worker_permission_denied(self):
#         """
#         Test creating a flock breed by a farm worker (should be denied).
#         """
#         flock_breed_data = {"breed": FlockBreedTypeChoices.BANTAM}
#         response = self.client.post(
#             reverse("poultry:flock-breeds-list"),
#             flock_breed_data,
#             HTTP_AUTHORIZATION=f"Token {self.farm_worker_token}",
#         )
#         assert response.status_code == status.HTTP_403_FORBIDDEN
#         assert not FlockBreed.objects.filter(name=flock_breed_data["breed"]).exists()
#
#     def test_create_flock_breed_as_regular_user_permission_denied(self):
#         """
#         Test creating a flock breed by a regular user (should be denied).
#         """
#         flock_breed_data = {"breed": FlockBreedTypeChoices.RAINBOW_ROOSTER}
#         response = self.client.post(
#             reverse("poultry:flock-breeds-list"),
#             flock_breed_data,
#             HTTP_AUTHORIZATION=f"Token {self.regular_user_token}",
#         )
#         assert response.status_code == status.HTTP_403_FORBIDDEN
#         assert not FlockBreed.objects.filter(name=flock_breed_data["breed"]).exists()
#
#     def test_create_flock_breed_without_authentication(self):
#         """
#         Test creating a flock breed without authentication (should be denied).
#         """
#         flock_breed_data = {"breed": FlockBreedTypeChoices.RAINBOW_ROOSTER}
#         response = self.client.post(
#             reverse("poultry:flock-breeds-list"), flock_breed_data
#         )
#         assert response.status_code == status.HTTP_401_UNAUTHORIZED
#         assert not FlockBreed.objects.filter(name=flock_breed_data["breed"]).exists()
#
#     def test_retrieve_flock_breeds_as_farm_owner(self):
#         """
#         Test retrieving flock breeds by a farm owner.
#         """
#         response = self.client.get(
#             reverse("poultry:flock-breeds-list"),
#             HTTP_AUTHORIZATION=f"Token {self.farm_owner_token}",
#         )
#         assert response.status_code == status.HTTP_200_OK
#
#     def test_retrieve_flock_breeds_as_farm_manager(self):
#         """
#         Test retrieving flock breeds by a farm manager.
#         """
#         response = self.client.get(
#             reverse("poultry:flock-breeds-list"),
#             HTTP_AUTHORIZATION=f"Token {self.farm_manager_token}",
#         )
#         assert response.status_code == status.HTTP_200_OK
#
#     def test_retrieve_flock_breeds_as_asst_farm_manager(self):
#         """
#         Test retrieving flock breeds by an assistant farm manager.
#         """
#         response = self.client.get(
#             reverse("poultry:flock-breeds-list"),
#             HTTP_AUTHORIZATION=f"Token {self.asst_farm_manager_token}",
#         )
#         assert response.status_code == status.HTTP_200_OK
#
#     def test_retrieve_flock_breeds_as_team_leader(self):
#         """
#         Test retrieving flock breeds by a team leader.
#         """
#         response = self.client.get(
#             reverse("poultry:flock-breeds-list"),
#             HTTP_AUTHORIZATION=f"Token {self.team_leader_token}",
#         )
#         assert response.status_code == status.HTTP_200_OK
#
#     def test_retrieve_flock_breed_as_regular_user_permission_denied(self):
#         """
#         Test retrieving flock breeds by a regular user (should be denied).
#         """
#         response = self.client.get(
#             reverse("poultry:flock-breeds-list"),
#             HTTP_AUTHORIZATION=f"Token {self.regular_user_token}",
#         )
#         assert response.status_code == status.HTTP_403_FORBIDDEN
#
#     def test_retrieve_flock_breed_without_authentication(self):
#         """
#         Test retrieving flock breeds without authentication (should be denied).
#         """
#         url = reverse("poultry:flock-breeds-list")
#         response = self.client.get(url)
#         assert response.status_code == status.HTTP_401_UNAUTHORIZED
#
#     def test_update_flock_breed_permission_denied(self):
#         """
#         Test updating a flock breed (should be denied).
#         """
#         flock_breed = FlockBreed.objects.create(
#             name=FlockBreedTypeChoices.RAINBOW_ROOSTER
#         )
#         url = reverse("poultry:flock-breeds-detail", kwargs={"pk": flock_breed.id})
#         flock_breed_update_data = {"breed": FlockBreedTypeChoices.RAINBOW_ROOSTER}
#         response = self.client.put(
#             url,
#             flock_breed_update_data,
#             HTTP_AUTHORIZATION=f"Token {self.farm_owner_token}",
#         )
#         assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
#
#     def test_delete_flock_breed_as_farm_owner(self):
#         """
#         Test deleting a flock breed by a farm owner.
#         """
#         flock_breed = FlockBreed.objects.create(
#             name=FlockBreedTypeChoices.RAINBOW_ROOSTER
#         )
#         url = reverse("poultry:flock-breeds-detail", kwargs={"pk": flock_breed.id})
#         response = self.client.delete(
#             url, HTTP_AUTHORIZATION=f"Token {self.farm_owner_token}"
#         )
#         assert response.status_code == status.HTTP_204_NO_CONTENT
#         assert not FlockBreed.objects.filter(id=flock_breed.id).exists()
#
#     def test_delete_flock_breed_as_farm_manager(self):
#         """
#         Test deleting a flock breed by a farm manager.
#         """
#         flock_breed = FlockBreed.objects.create(
#             name=FlockBreedTypeChoices.RAINBOW_ROOSTER
#         )
#         url = reverse("poultry:flock-breeds-detail", kwargs={"pk": flock_breed.id})
#         response = self.client.delete(
#             url, HTTP_AUTHORIZATION=f"Token {self.farm_manager_token}"
#         )
#         assert response.status_code == status.HTTP_204_NO_CONTENT
#         assert not FlockBreed.objects.filter(id=flock_breed.id).exists()
#
#     def test_delete_flock_breed_as_asst_farm_manager_permission_denied(self):
#         """
#         Test deleting a flock breed by an assistant farm manager (should be denied).
#         """
#         flock_breed = FlockBreed.objects.create(
#             name=FlockBreedTypeChoices.RAINBOW_ROOSTER
#         )
#         url = reverse("poultry:flock-breeds-detail", kwargs={"pk": flock_breed.id})
#         response = self.client.delete(
#             url, HTTP_AUTHORIZATION=f"Token {self.asst_farm_manager_token}"
#         )
#         assert response.status_code == status.HTTP_403_FORBIDDEN
#         assert FlockBreed.objects.filter(id=flock_breed.id).exists()
#
#     def test_delete_flock_breed_as_team_leader_permission_denied(self):
#         """
#         Test deleting a flock breed by a team leader (should be denied).
#         """
#         flock_breed = FlockBreed.objects.create(
#             name=FlockBreedTypeChoices.RAINBOW_ROOSTER
#         )
#         url = reverse("poultry:flock-breeds-detail", kwargs={"pk": flock_breed.id})
#         response = self.client.delete(
#             url, HTTP_AUTHORIZATION=f"Token {self.team_leader_token}"
#         )
#         assert response.status_code == status.HTTP_403_FORBIDDEN
#         assert FlockBreed.objects.filter(id=flock_breed.id).exists()
#
#     def test_delete_flock_breed_as_farm_worker_permission_denied(self):
#         """
#         Test deleting a flock breed by a farm worker (should be denied).
#         """
#         flock_breed = FlockBreed.objects.create(
#             name=FlockBreedTypeChoices.RAINBOW_ROOSTER
#         )
#         url = reverse("poultry:flock-breeds-detail", kwargs={"pk": flock_breed.id})
#         response = self.client.delete(
#             url, HTTP_AUTHORIZATION=f"Token {self.farm_worker_token}"
#         )
#         assert response.status_code == status.HTTP_403_FORBIDDEN
#         assert FlockBreed.objects.filter(id=flock_breed.id).exists()
#
#     def test_delete_flock_breed_as_regular_user_permission_denied(self):
#         """
#         Test delete flock breed as a regular user (permission denied)
#         """
#         flock_breed = FlockBreed.objects.create(
#             name=FlockBreedTypeChoices.RAINBOW_ROOSTER
#         )
#         url = reverse("poultry:flock-breeds-detail", kwargs={"pk": flock_breed.id})
#
#         response = self.client.delete(
#             url, HTTP_AUTHORIZATION=f"Token {self.regular_user_token}"
#         )
#         assert response.status_code == status.HTTP_403_FORBIDDEN
#         assert FlockBreed.objects.filter(id=flock_breed.id).exists()
#
#     def test_delete_flock_breed_unauthorized(self):
#         """
#         Test delete flock breed by unauthorized request
#         """
#         flock_breed = FlockBreed.objects.create(
#             name=FlockBreedTypeChoices.RAINBOW_ROOSTER
#         )
#         url = reverse("poultry:flock-breeds-detail", kwargs={"pk": flock_breed.id})
#
#         response = self.client.delete(url)
#         assert response.status_code == status.HTTP_401_UNAUTHORIZED
#         assert FlockBreed.objects.filter(id=flock_breed.id).exists()
#
#     def test_filter_flock_breed_by_breed(self):
#         """
#         Test filtering flock breeds by breed (e.g., get all breeds with breed 'KIPLELS_FARM').
#         """
#         FlockBreed.objects.create(name=FlockBreedTypeChoices.BRAHMA)
#         FlockBreed.objects.create(name=FlockBreedTypeChoices.INDIGENOUS)
#         url = reverse("poultry:flock-breeds-list")
#         url += f"?name={FlockBreedTypeChoices.INDIGENOUS}"
#
#         response = self.client.get(
#             url, HTTP_AUTHORIZATION=f"Token {self.farm_owner_token}"
#         )
#
#         assert response.status_code == status.HTTP_200_OK
#         assert len(response.data) == 1
#         assert response.data[0]["name"] == FlockBreedTypeChoices.INDIGENOUS
#
#     def test_filter_flock_breed_by_partial_breed(self):
#         """
#         Test filtering flock breeds by partial breed (e.g., get breeds with breeds containing 'ey').
#         """
#         FlockBreed.objects.create(name=FlockBreedTypeChoices.COCHIN)
#         FlockBreed.objects.create(name=FlockBreedTypeChoices.LEGHORN)
#         url = reverse("poultry:flock-breeds-list")
#         url += "?name=leg"
#
#         response = self.client.get(
#             url, HTTP_AUTHORIZATION=f"Token {self.asst_farm_manager_token}"
#         )
#         assert response.status_code == status.HTTP_200_OK
#         assert len(response.data) == 1
#
#     def test_order_flock_breed_by_multiple_fields(self):
#         """
#         Test ordering flock breeds by multiple fields (e.g., breed in descending order, id in ascending order).
#         """
#         FlockBreed.objects.create(name=FlockBreedTypeChoices.RAINBOW_ROOSTER)
#         FlockBreed.objects.create(name=FlockBreedTypeChoices.EASTER_EGGER)
#         FlockBreed.objects.create(name=FlockBreedTypeChoices.INDIGENOUS)
#         FlockBreed.objects.create(name=FlockBreedTypeChoices.LEGHORN)
#
#         url = reverse("poultry:flock-breeds-list")
#         url += "?ordering=-name"
#
#         response = self.client.get(
#             url, HTTP_AUTHORIZATION=f"Token {self.farm_manager_token}"
#         )
#         assert response.status_code == status.HTTP_200_OK
#         assert len(response.data) == 4
#         assert response.data[0]["name"] == FlockBreedTypeChoices.RAINBOW_ROOSTER
#         assert response.data[1]["name"] == FlockBreedTypeChoices.LEGHORN
#         assert response.data[2]["name"] == FlockBreedTypeChoices.INDIGENOUS
#         assert response.data[3]["name"] == FlockBreedTypeChoices.EASTER_EGGER
#
#     def test_no_results_for_invalid_breed(self):
#         """
#         Test filtering with a breed that doesn't exist.
#         """
#         url = reverse("poultry:flock-breeds-list")
#         url += "?name=nonexistent"
#         response = self.client.get(
#             url, HTTP_AUTHORIZATION=f"Token {self.farm_worker_token}"
#         )
#         assert response.status_code == status.HTTP_404_NOT_FOUND
#         assert response.data == {
#             "detail": "No flock breed(s) found matching the provided filters."
#         }
#
#
# @pytest.mark.django_db
# class TestHousingStructureViewSet:
#     @pytest.fixture(autouse=True)
#     def setup(self, setup_users, setup_housing_structure_data):
#         self.client = setup_users["client"]
#
#         self.regular_user_token = setup_users["regular_user_token"]
#         self.farm_owner_token = setup_users["farm_owner_token"]
#         self.farm_manager_token = setup_users["farm_manager_token"]
#         self.asst_farm_manager_token = setup_users["asst_farm_manager_token"]
#         self.team_leader_token = setup_users["team_leader_token"]
#         self.farm_worker_token = setup_users["farm_worker_token"]
#
#         self.housing_structure_data = setup_housing_structure_data[
#             "housing_structure_data"
#         ]
#
#     def test_create_housing_structure_as_farm_owner(self):
#         """
#         Test create housing structure by a farm owner.
#         """
#         response = self.client.post(
#             reverse("poultry:housing-structures-list"),
#             data=self.housing_structure_data,
#             HTTP_AUTHORIZATION=f"Token {self.farm_owner_token}",
#         )
#         assert response.status_code == status.HTTP_201_CREATED
#         assert HousingStructure.objects.filter(
#             house_type=self.housing_structure_data["house_type"]
#         ).exists()
#
#     def test_create_housing_structure_as_farm_manager(self):
#         """
#         Test add housing structure by a farm manager.
#         """
#         response = self.client.post(
#             reverse("poultry:housing-structures-list"),
#             self.housing_structure_data,
#             HTTP_AUTHORIZATION=f"Token {self.farm_manager_token}",
#         )
#         assert response.status_code == status.HTTP_201_CREATED
#         assert HousingStructure.objects.filter(
#             house_type=self.housing_structure_data["house_type"]
#         ).exists()
#
#     def test_create_housing_structure_as_asst_farm_manager_permission_denied(self):
#         """
#         Test creating a housing structure by an assistant farm manager (should be denied).
#         """
#
#         response = self.client.post(
#             reverse("poultry:housing-structures-list"),
#             self.housing_structure_data,
#             HTTP_AUTHORIZATION=f"Token {self.asst_farm_manager_token}",
#         )
#         assert response.status_code == status.HTTP_403_FORBIDDEN
#         assert not HousingStructure.objects.filter(
#             house_type=self.housing_structure_data["house_type"]
#         ).exists()
#
#     def test_create_housing_structure_as_team_leader_permission_denied(self):
#         """
#         Test creating a housing structure by a team leader (should be denied).
#         """
#
#         response = self.client.post(
#             reverse("poultry:housing-structures-list"),
#             self.housing_structure_data,
#             HTTP_AUTHORIZATION=f"Token {self.team_leader_token}",
#         )
#         assert response.status_code == status.HTTP_403_FORBIDDEN
#         assert not HousingStructure.objects.filter(
#             house_type=self.housing_structure_data["house_type"]
#         ).exists()
#
#     def test_create_housing_structure_as_farm_worker_permission_denied(self):
#         """
#         Test creating a housing structure by a farm worker (should be denied).
#         """
#         response = self.client.post(
#             reverse("poultry:housing-structures-list"),
#             self.housing_structure_data,
#             HTTP_AUTHORIZATION=f"Token {self.farm_worker_token}",
#         )
#         assert response.status_code == status.HTTP_403_FORBIDDEN
#         assert not HousingStructure.objects.filter(
#             house_type=self.housing_structure_data["house_type"]
#         ).exists()
#
#     def test_create_housing_structure_as_regular_user_permission_denied(self):
#         """
#         Test creating a housing structure by a regular user (should be denied).
#         """
#         response = self.client.post(
#             reverse("poultry:housing-structures-list"),
#             self.housing_structure_data,
#             HTTP_AUTHORIZATION=f"Token {self.regular_user_token}",
#         )
#         assert response.status_code == status.HTTP_403_FORBIDDEN
#         assert not HousingStructure.objects.filter(
#             house_type=self.housing_structure_data["house_type"]
#         ).exists()
#
#     def test_create_housing_structure_without_authentication(self):
#         """
#         Test creating a housing structure without authentication (should be denied).
#         """
#
#         response = self.client.post(
#             reverse("poultry:housing-structures-list"), self.housing_structure_data
#         )
#         assert response.status_code == status.HTTP_401_UNAUTHORIZED
#         assert not HousingStructure.objects.filter(
#             house_type=self.housing_structure_data["house_type"]
#         ).exists()
#
#     def test_retrieve_housing_structures_as_farm_owner(self):
#         """
#         Test retrieving housing structures by a farm owner.
#         """
#         response = self.client.get(
#             reverse("poultry:housing-structures-list"),
#             HTTP_AUTHORIZATION=f"Token {self.farm_owner_token}",
#         )
#         assert response.status_code == status.HTTP_200_OK
#
#     def test_retrieve_housing_structures_as_farm_manager(self):
#         """
#         Test retrieving housing structures by a farm manager.
#         """
#         response = self.client.get(
#             reverse("poultry:housing-structures-list"),
#             HTTP_AUTHORIZATION=f"Token {self.farm_manager_token}",
#         )
#         assert response.status_code == status.HTTP_200_OK
#
#     def test_retrieve_housing_structures_as_asst_farm_manager_permission_denied(self):
#         """
#         Test retrieving housing structures by an assistant farm manager (should be denied).
#         """
#         response = self.client.get(
#             reverse("poultry:housing-structures-list"),
#             HTTP_AUTHORIZATION=f"Token {self.asst_farm_manager_token}",
#         )
#         assert response.status_code == status.HTTP_403_FORBIDDEN
#
#     def test_retrieve_housing_structures_as_team_leader_permission_denied(self):
#         """
#         Test retrieving housing structures by a team leader (should be denied).
#         """
#         response = self.client.get(
#             reverse("poultry:housing-structures-list"),
#             HTTP_AUTHORIZATION=f"Token {self.team_leader_token}",
#         )
#         assert response.status_code == status.HTTP_403_FORBIDDEN
#
#     def test_retrieve_housing_structure_as_regular_user_permission_denied(self):
#         """
#         Test retrieving housing structures by a regular user (should be denied).
#         """
#         response = self.client.get(
#             reverse("poultry:housing-structures-list"),
#             HTTP_AUTHORIZATION=f"Token {self.regular_user_token}",
#         )
#         assert response.status_code == status.HTTP_403_FORBIDDEN
#
#     def test_retrieve_housing_structure_without_authentication(self):
#         """
#         Test retrieving housing structures without authentication (should be denied).
#         """
#         url = reverse("poultry:housing-structures-list")
#         response = self.client.get(url)
#         assert response.status_code == status.HTTP_401_UNAUTHORIZED
#
#     def test_update_housing_structure_as_farm_owner(self):
#         """
#         Test updating a housing structure as farm owner.
#         """
#         serializer = HousingStructureSerializer(data=self.housing_structure_data)
#         serializer.is_valid()
#         housing_structure = serializer.save()
#
#         housing_structure_data_update_data = {
#             "house_type": HousingStructureTypeChoices.CLOSED_SHED,
#             "category": HousingStructureCategoryChoices.BREEDERS_HOUSE,
#         }
#         response = self.client.put(
#             reverse(
#                 "poultry:housing-structures-detail", kwargs={"pk": housing_structure.id}
#             ),
#             housing_structure_data_update_data,
#             HTTP_AUTHORIZATION=f"Token {self.farm_owner_token}",
#         )
#         assert response.status_code == status.HTTP_200_OK
#
#     def test_update_housing_structure_as_farm_manager(self):
#         """
#         Test updating a housing structure as farm manager.
#         """
#         serializer = HousingStructureSerializer(data=self.housing_structure_data)
#         serializer.is_valid()
#         housing_structure = serializer.save()
#
#         housing_structure_data_update_data = {
#             "house_type": HousingStructureTypeChoices.CLOSED_SHED,
#             "category": HousingStructureCategoryChoices.BREEDERS_HOUSE,
#         }
#         response = self.client.put(
#             reverse(
#                 "poultry:housing-structures-detail", kwargs={"pk": housing_structure.id}
#             ),
#             housing_structure_data_update_data,
#             HTTP_AUTHORIZATION=f"Token {self.farm_manager_token}",
#         )
#         assert response.status_code == status.HTTP_200_OK
#
#     def test_update_housing_structure_as_assistant_farm_manager_permission_denied(self):
#         """
#         Test updating a housing structure as assistant farm manager (should be denied).
#         """
#         serializer = HousingStructureSerializer(data=self.housing_structure_data)
#         serializer.is_valid()
#         housing_structure = serializer.save()
#
#         housing_structure_data_update_data = {
#             "house_type": HousingStructureTypeChoices.CLOSED_SHED,
#             "category": HousingStructureCategoryChoices.BREEDERS_HOUSE,
#         }
#         response = self.client.put(
#             reverse(
#                 "poultry:housing-structures-detail", kwargs={"pk": housing_structure.id}
#             ),
#             housing_structure_data_update_data,
#             HTTP_AUTHORIZATION=f"Token {self.asst_farm_manager_token}",
#         )
#         assert response.status_code == status.HTTP_403_FORBIDDEN
#
#     def test_update_housing_structure_as_team_leader_permission_denied(self):
#         """
#         Test updating a housing structure as team leader (should be denied).
#         """
#         serializer = HousingStructureSerializer(data=self.housing_structure_data)
#         serializer.is_valid()
#         housing_structure = serializer.save()
#
#         housing_structure_data_update_data = {
#             "house_type": HousingStructureTypeChoices.CLOSED_SHED,
#             "category": HousingStructureCategoryChoices.BREEDERS_HOUSE,
#         }
#         response = self.client.put(
#             reverse(
#                 "poultry:housing-structures-detail", kwargs={"pk": housing_structure.id}
#             ),
#             housing_structure_data_update_data,
#             HTTP_AUTHORIZATION=f"Token {self.team_leader_token}",
#         )
#         assert response.status_code == status.HTTP_403_FORBIDDEN
#
#     def test_update_housing_structure_as_farm_worker_permission_denied(self):
#         """
#         Test updating a housing structure as farm worker (should be denied).
#         """
#         serializer = HousingStructureSerializer(data=self.housing_structure_data)
#         serializer.is_valid()
#         housing_structure = serializer.save()
#
#         housing_structure_data_update_data = {
#             "house_type": HousingStructureTypeChoices.CLOSED_SHED,
#             "category": HousingStructureCategoryChoices.BREEDERS_HOUSE,
#         }
#         response = self.client.put(
#             reverse(
#                 "poultry:housing-structures-detail", kwargs={"pk": housing_structure.id}
#             ),
#             housing_structure_data_update_data,
#             HTTP_AUTHORIZATION=f"Token {self.farm_worker_token}",
#         )
#         assert response.status_code == status.HTTP_403_FORBIDDEN
#
#     def test_update_housing_structure_as_regular_user_permission_denied(self):
#         """
#         Test updating a housing structure as regular user (should be denied).
#         """
#         serializer = HousingStructureSerializer(data=self.housing_structure_data)
#         serializer.is_valid()
#         housing_structure = serializer.save()
#
#         housing_structure_data_update_data = {
#             "house_type": HousingStructureTypeChoices.CLOSED_SHED,
#             "category": HousingStructureCategoryChoices.BREEDERS_HOUSE,
#         }
#         response = self.client.put(
#             reverse(
#                 "poultry:housing-structures-detail", kwargs={"pk": housing_structure.id}
#             ),
#             housing_structure_data_update_data,
#             HTTP_AUTHORIZATION=f"Token {self.regular_user_token}",
#         )
#         assert response.status_code == status.HTTP_403_FORBIDDEN
#
#     def test_update_housing_structure_without_authentication(self):
#         """
#         Test updating a housing structure without authentication (should be denied).
#         """
#         serializer = HousingStructureSerializer(data=self.housing_structure_data)
#         serializer.is_valid()
#         housing_structure = serializer.save()
#
#         housing_structure_data_update_data = {
#             "house_type": HousingStructureTypeChoices.CLOSED_SHED,
#             "category": HousingStructureCategoryChoices.BREEDERS_HOUSE,
#         }
#         response = self.client.put(
#             reverse(
#                 "poultry:housing-structures-detail", kwargs={"pk": housing_structure.id}
#             ),
#             housing_structure_data_update_data,
#         )
#         assert response.status_code == status.HTTP_401_UNAUTHORIZED
#
#     def test_delete_housing_structure_as_farm_owner(self):
#         """
#         Test deleting a housing structure by a farm owner.
#         """
#         serializer = HousingStructureSerializer(data=self.housing_structure_data)
#         serializer.is_valid()
#         housing_structure = serializer.save()
#
#         response = self.client.delete(
#             reverse(
#                 "poultry:housing-structures-detail", kwargs={"pk": housing_structure.id}
#             ),
#             HTTP_AUTHORIZATION=f"Token {self.farm_owner_token}",
#         )
#         assert response.status_code == status.HTTP_204_NO_CONTENT
#         assert not HousingStructure.objects.filter(id=housing_structure.id).exists()
#
#     def test_delete_housing_structure_as_farm_manager(self):
#         """
#         Test deleting a housing structure by a farm manager.
#         """
#         serializer = HousingStructureSerializer(data=self.housing_structure_data)
#         serializer.is_valid()
#         housing_structure = serializer.save()
#
#         response = self.client.delete(
#             reverse(
#                 "poultry:housing-structures-detail", kwargs={"pk": housing_structure.id}
#             ),
#             HTTP_AUTHORIZATION=f"Token {self.farm_manager_token}",
#         )
#         assert response.status_code == status.HTTP_204_NO_CONTENT
#         assert not HousingStructure.objects.filter(id=housing_structure.id).exists()
#
#     def test_delete_housing_structure_as_asst_farm_manager_permission_denied(self):
#         """
#         Test deleting a housing structure by an assistant farm manager (should be denied).
#         """
#         serializer = HousingStructureSerializer(data=self.housing_structure_data)
#         serializer.is_valid()
#         housing_structure = serializer.save()
#
#         response = self.client.delete(
#             reverse(
#                 "poultry:housing-structures-detail", kwargs={"pk": housing_structure.id}
#             ),
#             HTTP_AUTHORIZATION=f"Token {self.asst_farm_manager_token}",
#         )
#         assert response.status_code == status.HTTP_403_FORBIDDEN
#         assert HousingStructure.objects.filter(id=housing_structure.id).exists()
#
#     def test_delete_housing_structure_as_team_leader_permission_denied(self):
#         """
#         Test deleting a housing structure by a team leader (should be denied).
#         """
#         serializer = HousingStructureSerializer(data=self.housing_structure_data)
#         serializer.is_valid()
#         housing_structure = serializer.save()
#
#         response = self.client.delete(
#             reverse(
#                 "poultry:housing-structures-detail", kwargs={"pk": housing_structure.id}
#             ),
#             HTTP_AUTHORIZATION=f"Token {self.team_leader_token}",
#         )
#         assert response.status_code == status.HTTP_403_FORBIDDEN
#         assert HousingStructure.objects.filter(id=housing_structure.id).exists()
#
#     def test_delete_housing_structure_as_farm_worker_permission_denied(self):
#         """
#         Test deleting a housing structure by a farm worker (should be denied).
#         """
#         serializer = HousingStructureSerializer(data=self.housing_structure_data)
#         serializer.is_valid()
#         housing_structure = serializer.save()
#
#         response = self.client.delete(
#             reverse(
#                 "poultry:housing-structures-detail", kwargs={"pk": housing_structure.id}
#             ),
#             HTTP_AUTHORIZATION=f"Token {self.farm_worker_token}",
#         )
#         assert response.status_code == status.HTTP_403_FORBIDDEN
#         assert HousingStructure.objects.filter(id=housing_structure.id).exists()
#
#     def test_delete_housing_structure_as_regular_user_permission_denied(self):
#         """
#         Test delete housing structure as a regular user (permission denied)
#         """
#         serializer = HousingStructureSerializer(data=self.housing_structure_data)
#         serializer.is_valid()
#         housing_structure = serializer.save()
#
#         response = self.client.delete(
#             reverse(
#                 "poultry:housing-structures-detail", kwargs={"pk": housing_structure.id}
#             ),
#             HTTP_AUTHORIZATION=f"Token {self.regular_user_token}",
#         )
#         assert response.status_code == status.HTTP_403_FORBIDDEN
#         assert HousingStructure.objects.filter(id=housing_structure.id).exists()
#
#     def test_delete_housing_structure_unauthorized(self):
#         """
#         Test delete housing structure by unauthorized request
#         """
#         serializer = HousingStructureSerializer(data=self.housing_structure_data)
#         serializer.is_valid()
#         housing_structure = serializer.save()
#
#         response = self.client.delete(
#             reverse(
#                 "poultry:housing-structures-detail", kwargs={"pk": housing_structure.id}
#             )
#         )
#         assert response.status_code == status.HTTP_401_UNAUTHORIZED
#         assert HousingStructure.objects.filter(id=housing_structure.id).exists()
#
#     def test_filter_housing_structure_by_category(self):
#         """
#         Test filtering housing structures by category.
#         """
#         serializer = HousingStructureSerializer(data=self.housing_structure_data)
#         serializer.is_valid()
#         serializer.save()
#         url = reverse("poultry:housing-structures-list")
#         url += f"?category={HousingStructureCategoryChoices.BROODER_CHICK_HOUSE}"
#
#         response = self.client.get(
#             url, HTTP_AUTHORIZATION=f"Token {self.farm_owner_token}"
#         )
#
#         assert response.status_code == status.HTTP_200_OK
#         assert len(response.data) == 1
#         assert (
#             response.data[0]["category"]
#             == HousingStructureCategoryChoices.BROODER_CHICK_HOUSE
#         )


@pytest.mark.django_db
class TestFlockViewSet:
    @pytest.fixture(autouse=True)
    def setup(self, setup_users, setup_flock_data):
        self.client = setup_users["client"]

        self.regular_user_token = setup_users["regular_user_token"]
        self.farm_owner_token = setup_users["farm_owner_token"]
        self.farm_manager_token = setup_users["farm_manager_token"]
        self.asst_farm_manager_token = setup_users["asst_farm_manager_token"]
        self.team_leader_token = setup_users["team_leader_token"]
        self.farm_worker_token = setup_users["farm_worker_token"]

        self.flock_data = setup_flock_data["flock_data"]

    def test_add_flock_as_farm_owner(self):
        """
        Test add flock by a farm owner.
        """
        response = self.client.post(
            reverse("poultry:flocks-list"),
            data=self.flock_data,
            HTTP_AUTHORIZATION=f"Token {self.farm_owner_token}",
            format="json",
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert Flock.objects.filter(
            chicken_type=self.flock_data["chicken_type"]
        ).exists()

    def test_add_flock_as_farm_manager(self):
        """
        Test add flock by a farm manager.
        """
        response = self.client.post(
            reverse("poultry:flocks-list"),
            data=self.flock_data,
            HTTP_AUTHORIZATION=f"Token {self.farm_manager_token}",
            format="json",
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert Flock.objects.filter(
            chicken_type=self.flock_data["chicken_type"]
        ).exists()

    def test_add_flock_as_asst_farm_manager_permission_denied(self):
        """
        Test add flock by an assistant farm manager (should be denied).
        """
        response = self.client.post(
            reverse("poultry:flocks-list"),
            data=self.flock_data,
            HTTP_AUTHORIZATION=f"Token {self.asst_farm_manager_token}",
            format="json",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not Flock.objects.filter(
            chicken_type=self.flock_data["chicken_type"]
        ).exists()

    def test_add_flock_as_team_leader_permission_denied(self):
        """
        Test add flock by a team leader (should be denied).
        """
        response = self.client.post(
            reverse("poultry:flocks-list"),
            data=self.flock_data,
            HTTP_AUTHORIZATION=f"Token {self.team_leader_token}",
            format="json",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not Flock.objects.filter(
            chicken_type=self.flock_data["chicken_type"]
        ).exists()

    def test_add_flock_as_a_farm_worker_permission_denied(self):
        """
        Test add flock by a farm worker (should be denied).
        """
        response = self.client.post(
            reverse("poultry:flocks-list"),
            data=self.flock_data,
            HTTP_AUTHORIZATION=f"Token {self.farm_worker_token}",
            format="json",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not Flock.objects.filter(
            chicken_type=self.flock_data["chicken_type"]
        ).exists()

    def test_add_flock_as_regular_user_permission_denied(self):
        """
        Test add flock by a regular user (should be denied).
        """
        response = self.client.post(
            reverse("poultry:flocks-list"),
            data=self.flock_data,
            HTTP_AUTHORIZATION=f"Token {self.regular_user_token}",
            format="json",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not Flock.objects.filter(
            chicken_type=self.flock_data["chicken_type"]
        ).exists()

    def test_add_flock_without_authentication(self):
        """
        Test add flock without authentication (should be denied).
        """
        response = self.client.post(
            reverse("poultry:flocks-list"), data=self.flock_data, format="json"
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert not Flock.objects.filter(
            chicken_type=self.flock_data["chicken_type"]
        ).exists()

    def test_retrieve_flocks_as_farm_owner(self):
        """
        Test retrieving flocks by a farm owner.
        """
        response = self.client.get(
            reverse("poultry:flocks-list"),
            HTTP_AUTHORIZATION=f"Token {self.farm_owner_token}",
        )
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_flocks_as_farm_manager(self):
        """
        Test retrieving flocks by a farm manager.
        """
        response = self.client.get(
            reverse("poultry:flocks-list"),
            HTTP_AUTHORIZATION=f"Token {self.farm_manager_token}",
        )
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_flocks_as_asst_farm_manager(self):
        """
        Test retrieving flocks by an assistant farm manager.
        """
        response = self.client.get(
            reverse("poultry:flocks-list"),
            HTTP_AUTHORIZATION=f"Token {self.asst_farm_manager_token}",
        )
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_flocks_as_team_leader(self):
        """
        Test retrieving flocks by a team leader.
        """
        response = self.client.get(
            reverse("poultry:flocks-list"),
            HTTP_AUTHORIZATION=f"Token {self.team_leader_token}",
        )
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_flock_as_regular_user_permission_denied(self):
        """
        Test retrieving flocks by a regular user (should be denied).
        """
        response = self.client.get(
            reverse("poultry:flocks-list"),
            HTTP_AUTHORIZATION=f"Token {self.regular_user_token}",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_retrieve_flock_without_authentication(self):
        """
        Test retrieving flocks without authentication (should be denied).
        """
        url = reverse("poultry:flocks-list")
        response = self.client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_flock_as_farm_owner(self):
        """
        Test updating a flock as farm owner.
        """
        serializer = FlockSerializer(data=self.flock_data)
        serializer.is_valid()
        flock = serializer.save()

        flock_data_update_data = {
            "current_rearing_method": RearingMethodChoices.CAGE_SYSTEM,
        }
        response = self.client.patch(
            reverse("poultry:flocks-detail", kwargs={"pk": flock.id}),
            flock_data_update_data,
            HTTP_AUTHORIZATION=f"Token {self.farm_owner_token}",
        )
        assert response.status_code == status.HTTP_200_OK

    def test_update_flock_as_farm_manager(self):
        """
        Test updating a flock as farm manager.
        """
        serializer = FlockSerializer(data=self.flock_data)
        serializer.is_valid()
        flock = serializer.save()

        print(FlockHistory.objects.all().count())
        update_data = {"current_rearing_methodgdsgsd": RearingMethodChoices.CAGE_SYSTEM}
        response = self.client.patch(
            reverse("poultry:flocks-detail", kwargs={"pk": flock.id}),
            data=update_data,
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.farm_manager_token}",
        )
        assert response.status_code == status.HTTP_200_OK
        print(FlockHistory.objects.all().count())

    def test_update_flock_as_assistant_farm_manager_permission_denied(self):
        """
        Test updating a flock as assistant farm manager (should be denied).
        """
        serializer = FlockSerializer(data=self.flock_data)
        serializer.is_valid()
        flock = serializer.save()

        flock_data_update_data = {
            "current_rearing_method": RearingMethodChoices.CAGE_SYSTEM,
        }
        response = self.client.put(
            reverse("poultry:flocks-detail", kwargs={"pk": flock.id}),
            flock_data_update_data,
            HTTP_AUTHORIZATION=f"Token {self.asst_farm_manager_token}",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_flock_as_team_leader_permission_denied(self):
        """
        Test updating a flock as team leader (should be denied).
        """
        serializer = FlockSerializer(data=self.flock_data)
        serializer.is_valid()
        flock = serializer.save()

        flock_data_update_data = {
            "current_rearing_method": RearingMethodChoices.CAGE_SYSTEM,
        }
        response = self.client.put(
            reverse("poultry:flocks-detail", kwargs={"pk": flock.id}),
            flock_data_update_data,
            HTTP_AUTHORIZATION=f"Token {self.team_leader_token}",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_flock_as_farm_worker_permission_denied(self):
        """
        Test updating a flock as farm worker (should be denied).
        """
        serializer = FlockSerializer(data=self.flock_data)
        serializer.is_valid()
        flock = serializer.save()

        flock_data_update_data = {
            "current_rearing_method": RearingMethodChoices.CAGE_SYSTEM,
        }
        response = self.client.put(
            reverse("poultry:flocks-detail", kwargs={"pk": flock.id}),
            flock_data_update_data,
            HTTP_AUTHORIZATION=f"Token {self.farm_worker_token}",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_flock_as_regular_user_permission_denied(self):
        """
        Test updating a flock as regular user (should be denied).
        """
        serializer = FlockSerializer(data=self.flock_data)
        serializer.is_valid()
        flock = serializer.save()

        flock_data_update_data = {
            "current_rearing_method": RearingMethodChoices.CAGE_SYSTEM,
        }
        response = self.client.put(
            reverse("poultry:flocks-detail", kwargs={"pk": flock.id}),
            flock_data_update_data,
            HTTP_AUTHORIZATION=f"Token {self.regular_user_token}",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_flock_without_authentication(self):
        """
        Test updating a flock without authentication (should be denied).
        """
        serializer = FlockSerializer(data=self.flock_data)
        serializer.is_valid()
        flock = serializer.save()

        flock_data_update_data = {
            "current_rearing_method": RearingMethodChoices.CAGE_SYSTEM,
        }
        response = self.client.put(
            reverse("poultry:flocks-detail", kwargs={"pk": flock.id}),
            flock_data_update_data,
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_flock_as_farm_owner(self):
        """
        Test deleting a flock by a farm owner.
        """
        serializer = FlockSerializer(data=self.flock_data)
        serializer.is_valid()
        flock = serializer.save()

        response = self.client.delete(
            reverse("poultry:flocks-detail", kwargs={"pk": flock.id}),
            HTTP_AUTHORIZATION=f"Token {self.farm_owner_token}",
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Flock.objects.filter(id=flock.id).exists()

    def test_delete_flock_as_farm_manager(self):
        """
        Test deleting a flock by a farm manager.
        """
        serializer = FlockSerializer(data=self.flock_data)
        serializer.is_valid()
        flock = serializer.save()

        response = self.client.delete(
            reverse("poultry:flocks-detail", kwargs={"pk": flock.id}),
            HTTP_AUTHORIZATION=f"Token {self.farm_manager_token}",
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Flock.objects.filter(id=flock.id).exists()

    def test_delete_flock_as_asst_farm_manager_permission_denied(self):
        """
        Test deleting a flock by an assistant farm manager (should be denied).
        """
        serializer = FlockSerializer(data=self.flock_data)
        serializer.is_valid()
        flock = serializer.save()

        response = self.client.delete(
            reverse("poultry:flocks-detail", kwargs={"pk": flock.id}),
            HTTP_AUTHORIZATION=f"Token {self.asst_farm_manager_token}",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Flock.objects.filter(id=flock.id).exists()

    def test_delete_flock_as_team_leader_permission_denied(self):
        """
        Test deleting a flock by a team leader (should be denied).
        """
        serializer = FlockSerializer(data=self.flock_data)
        serializer.is_valid()
        flock = serializer.save()

        response = self.client.delete(
            reverse("poultry:flocks-detail", kwargs={"pk": flock.id}),
            HTTP_AUTHORIZATION=f"Token {self.team_leader_token}",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Flock.objects.filter(id=flock.id).exists()

    def test_delete_flock_as_farm_worker_permission_denied(self):
        """
        Test deleting a flock by a farm worker (should be denied).
        """
        serializer = FlockSerializer(data=self.flock_data)
        serializer.is_valid()
        flock = serializer.save()

        response = self.client.delete(
            reverse("poultry:flocks-detail", kwargs={"pk": flock.id}),
            HTTP_AUTHORIZATION=f"Token {self.farm_worker_token}",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Flock.objects.filter(id=flock.id).exists()

    def test_delete_flock_as_regular_user_permission_denied(self):
        """
        Test delete flock as a regular user (permission denied)
        """
        serializer = FlockSerializer(data=self.flock_data)
        serializer.is_valid()
        flock = serializer.save()

        response = self.client.delete(
            reverse("poultry:flocks-detail", kwargs={"pk": flock.id}),
            HTTP_AUTHORIZATION=f"Token {self.regular_user_token}",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Flock.objects.filter(id=flock.id).exists()

    def test_delete_flock_unauthorized(self):
        """
        Test delete flock by unauthorized request
        """
        serializer = FlockSerializer(data=self.flock_data)
        serializer.is_valid()
        flock = serializer.save()

        response = self.client.delete(
            reverse("poultry:flocks-detail", kwargs={"pk": flock.id})
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert Flock.objects.filter(id=flock.id).exists()

    def test_filter_flock_by_chicken_type(self):
        """
        Test filtering flocks by category.
        """
        serializer = FlockSerializer(data=self.flock_data)
        serializer.is_valid()
        serializer.save()
        url = reverse("poultry:flocks-list")
        url += f"?chicken_type={ChickenTypeChoices.LAYERS}"

        response = self.client.get(
            url, HTTP_AUTHORIZATION=f"Token {self.farm_worker_token}"
        )

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["chicken_type"] == ChickenTypeChoices.LAYERS

    @pytest.mark.django_db
    class TestFlockHistoryViewSet:
        @pytest.fixture(autouse=True)
        def setup(self, setup_users, setup_flock_data):
            self.client = setup_users["client"]

            self.farm_owner_token = setup_users["farm_owner_token"]

            self.flock_data = setup_flock_data["flock_data"]

        def test_presence_of_flock_history_record(self):
            """
            Test add flock creates flock history.
            """
            serializer = FlockSerializer(data=self.flock_data)
            serializer.is_valid()
            flock = serializer.save()
            response = self.client.get(
                reverse("poultry:flock-histories-list"),
                HTTP_AUTHORIZATION=f"Token {self.farm_owner_token}",
            )
            assert len(response.data) == 1


@pytest.mark.django_db
class TestFlockHistoryViewSet:
    @pytest.fixture(autouse=True)
    def setup(self, setup_users, setup_flock_data):
        self.client = setup_users["client"]

        self.farm_owner_token = setup_users["farm_owner_token"]

        self.flock_data = setup_flock_data["flock_data"]

    def test_presence_of_flock_history_record(self):
        """
        Test add flock creates flock history.
        """
        serializer = FlockSerializer(data=self.flock_data)
        serializer.is_valid()
        flock = serializer.save()
        response = self.client.get(
            reverse("poultry:flock-histories-list"),
            HTTP_AUTHORIZATION=f"Token {self.farm_owner_token}",
        )
        assert len(response.data) == 1


@pytest.mark.django_db
class TestFlockMovementViewSet:
    @pytest.fixture(autouse=True)
    def setup(self, setup_users, setup_flock_movement_data):
        self.client = setup_users["client"]

        self.regular_user_token = setup_users["regular_user_token"]
        self.farm_owner_token = setup_users["farm_owner_token"]
        self.farm_manager_token = setup_users["farm_manager_token"]
        self.asst_farm_manager_token = setup_users["asst_farm_manager_token"]
        self.team_leader_token = setup_users["team_leader_token"]
        self.farm_worker_token = setup_users["farm_worker_token"]

        self.flock_movement_data = setup_flock_movement_data["flock_movement_data"]
        self.flock_movement_housing_update_data = setup_flock_movement_data[
            "housing_structure_3"
        ]

    def test_add_flock_movement_as_farm_owner(self):
        """
        Test add flock movement record by a farm owner.
        """
        response = self.client.post(
            reverse("poultry:flock-movements-list"),
            data=self.flock_movement_data,
            HTTP_AUTHORIZATION=f"Token {self.farm_owner_token}",
            format="json",
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert Flock.objects.filter(
            current_housing_structure=self.flock_movement_data["to_structure"]
        ).exists()

    def test_add_flock_movement_as_farm_manager(self):
        """
        Test add flock movement data by a farm manager.
        """
        response = self.client.post(
            reverse("poultry:flock-movements-list"),
            data=self.flock_movement_data,
            HTTP_AUTHORIZATION=f"Token {self.farm_manager_token}",
            format="json",
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert Flock.objects.filter(
            current_housing_structure=self.flock_movement_data["to_structure"]
        ).exists()

    def test_add_flock_movement_as_an_assistant_farm_manager_permission_denied(self):
        """
        Test add flock movement data by an assistant farm manager (permission denied).
        """
        response = self.client.post(
            reverse("poultry:flock-movements-list"),
            data=self.flock_movement_data,
            HTTP_AUTHORIZATION=f"Token {self.asst_farm_manager_token}",
            format="json",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not Flock.objects.filter(
            current_housing_structure=self.flock_movement_data["to_structure"]
        ).exists()

    def test_add_flock_movement_as_team_leader_permission_denied(self):
        """
        Test add flock movement data by a team leader (permission denied).
        """
        response = self.client.post(
            reverse("poultry:flock-movements-list"),
            data=self.flock_movement_data,
            HTTP_AUTHORIZATION=f"Token {self.team_leader_token}",
            format="json",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not Flock.objects.filter(
            current_housing_structure=self.flock_movement_data["to_structure"]
        ).exists()

    def test_add_flock_movement_as_farm_worker_permission_denied(self):
        """
        Test add flock movement data by a farm worker(permission denied).
        """
        response = self.client.post(
            reverse("poultry:flock-movements-list"),
            data=self.flock_movement_data,
            HTTP_AUTHORIZATION=f"Token {self.farm_worker_token}",
            format="json",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not Flock.objects.filter(
            current_housing_structure=self.flock_movement_data["to_structure"]
        ).exists()

    def test_add_flock_movement_as_regular_user_permission_denied(self):
        """
        Test add flock movement data by a regular user (permission denied).
        """
        response = self.client.post(
            reverse("poultry:flock-movements-list"),
            data=self.flock_movement_data,
            HTTP_AUTHORIZATION=f"Token {self.regular_user_token}",
            format="json",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not Flock.objects.filter(
            current_housing_structure=self.flock_movement_data["to_structure"]
        ).exists()

    def test_add_flock_movement_without_authentication(self):
        """
        Test add flock movement data without authentication. (permission denied).
        """
        response = self.client.post(
            reverse("poultry:flock-movements-list"),
            data=self.flock_movement_data,
            format="json",
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert not Flock.objects.filter(
            current_housing_structure=self.flock_movement_data["to_structure"]
        ).exists()

    def test_list_flock_movement_as_farm_owner(self):
        """
        Test list flock movement records by a farm owner.
        """
        response = self.client.get(
            reverse("poultry:flock-movements-list"),
            HTTP_AUTHORIZATION=f"Token {self.farm_owner_token}",
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK

    def test_list_flock_movement_as_farm_manager(self):
        """
        Test list flock movement records by a farm manager.
        """
        response = self.client.get(
            reverse("poultry:flock-movements-list"),
            HTTP_AUTHORIZATION=f"Token {self.farm_manager_token}",
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK

    def test_list_flock_movement_as_an_assistant_farm_manager_permission_denied(self):
        """
        Test list flock movement records by an assistant farm manager (permission denied).
        """
        response = self.client.get(
            reverse("poultry:flock-movements-list"),
            HTTP_AUTHORIZATION=f"Token {self.asst_farm_manager_token}",
            format="json",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_list_flock_movement_as_team_leader_permission_denied(self):
        """
        Test list flock movement records by a team leader (permission denied).
        """
        response = self.client.get(
            reverse("poultry:flock-movements-list"),
            HTTP_AUTHORIZATION=f"Token {self.team_leader_token}",
            format="json",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_list_flock_movement_as_farm_worker_permission_denied(self):
        """
        Test list flock movement data by a farm worker(permission denied).
        """
        response = self.client.get(
            reverse("poultry:flock-movements-list"),
            HTTP_AUTHORIZATION=f"Token {self.farm_worker_token}",
            format="json",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_list_flock_movement_as_regular_user_permission_denied(self):
        """
        Test list flock movement data by a regular user (permission denied).
        """
        response = self.client.get(
            reverse("poultry:flock-movements-list"),
            HTTP_AUTHORIZATION=f"Token {self.regular_user_token}",
            format="json",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_list_flock_movement_without_authentication(self):
        """
        Test list flock movement data without authentication. (permission denied).
        """
        response = self.client.get(
            reverse("poultry:flock-movements-list"), format="json"
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_flock_movement_as_farm_owner(self):
        """
        Test update flock movement records by a farm owner.
        """

        serializer = FlockMovementSerializer(data=self.flock_movement_data)
        serializer.is_valid()
        flock_movement = serializer.save()
        flock_movement_update_data = {
            "to_structure": self.flock_movement_housing_update_data
        }

        response = self.client.patch(
            reverse("poultry:flock-movements-detail", kwargs={"pk": flock_movement.id}),
            data=flock_movement_update_data,
            HTTP_AUTHORIZATION=f"Token {self.farm_owner_token}",
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK

    def test_update_flock_movement_as_farm_manager(self):
        """
        Test update flock movement records by a farm manager.
        """

        serializer = FlockMovementSerializer(data=self.flock_movement_data)
        serializer.is_valid()
        flock_movement = serializer.save()
        flock_movement_update_data = {
            "to_structure": self.flock_movement_housing_update_data
        }

        response = self.client.patch(
            reverse("poultry:flock-movements-detail", kwargs={"pk": flock_movement.id}),
            data=flock_movement_update_data,
            HTTP_AUTHORIZATION=f"Token {self.farm_manager_token}",
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK

    def test_update_flock_movement_as_assistant_farm_manager_permission_denied(self):
        """
        Test update flock movement records by an assistant farm manager (should be denied).
        """

        serializer = FlockMovementSerializer(data=self.flock_movement_data)
        serializer.is_valid()
        flock_movement = serializer.save()
        flock_movement_update_data = {
            "to_structure": self.flock_movement_housing_update_data
        }

        response = self.client.patch(
            reverse("poultry:flock-movements-detail", kwargs={"pk": flock_movement.id}),
            data=flock_movement_update_data,
            HTTP_AUTHORIZATION=f"Token {self.asst_farm_manager_token}",
            format="json",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_flock_movement_as_team_leader_permission_denied(self):
        """
        Test update flock movement records by a team leader (should be denied).
        """

        serializer = FlockMovementSerializer(data=self.flock_movement_data)
        serializer.is_valid()
        flock_movement = serializer.save()
        flock_movement_update_data = {
            "to_structure": self.flock_movement_housing_update_data
        }

        response = self.client.patch(
            reverse("poultry:flock-movements-detail", kwargs={"pk": flock_movement.id}),
            data=flock_movement_update_data,
            HTTP_AUTHORIZATION=f"Token {self.team_leader_token}",
            format="json",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_flock_movement_a_farm_worker_permission_denied(self):
        """
        Test update flock movement records by a farm worker (should be denied).
        """

        serializer = FlockMovementSerializer(data=self.flock_movement_data)
        serializer.is_valid()
        flock_movement = serializer.save()
        flock_movement_update_data = {
            "to_structure": self.flock_movement_housing_update_data
        }

        response = self.client.patch(
            reverse("poultry:flock-movements-detail", kwargs={"pk": flock_movement.id}),
            data=flock_movement_update_data,
            HTTP_AUTHORIZATION=f"Token {self.farm_worker_token}",
            format="json",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_flock_movement_a_regular_user_permission_denied(self):
        """
        Test update flock movement records by a regular user(should be denied).
        """

        serializer = FlockMovementSerializer(data=self.flock_movement_data)
        serializer.is_valid()
        flock_movement = serializer.save()
        flock_movement_update_data = {
            "to_structure": self.flock_movement_housing_update_data
        }

        response = self.client.patch(
            reverse("poultry:flock-movements-detail", kwargs={"pk": flock_movement.id}),
            data=flock_movement_update_data,
            HTTP_AUTHORIZATION=f"Token {self.regular_user_token}",
            format="json",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_flock_movement_without_authentication(self):
        """
        Test update flock movement records without authentication. (should be denied).
        """

        serializer = FlockMovementSerializer(data=self.flock_movement_data)
        serializer.is_valid()
        flock_movement = serializer.save()
        flock_movement_update_data = {
            "to_structure": self.flock_movement_housing_update_data
        }

        response = self.client.patch(
            reverse("poultry:flock-movements-detail", kwargs={"pk": flock_movement.id}),
            data=flock_movement_update_data,
            format="json",
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_flock_movement_as_farm_owner(self):
        """
        Test delete flock movement records by a farm owner.
        """

        serializer = FlockMovementSerializer(data=self.flock_movement_data)
        serializer.is_valid()
        flock_movement = serializer.save()

        response = self.client.delete(
            reverse("poultry:flock-movements-detail", kwargs={"pk": flock_movement.id}),
            HTTP_AUTHORIZATION=f"Token {self.farm_owner_token}",
            format="json",
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_flock_movement_as_farm_manager(self):
        """
        Test delete flock movement records by a farm manager.
        """

        serializer = FlockMovementSerializer(data=self.flock_movement_data)
        serializer.is_valid()
        flock_movement = serializer.save()

        response = self.client.delete(
            reverse("poultry:flock-movements-detail", kwargs={"pk": flock_movement.id}),
            HTTP_AUTHORIZATION=f"Token {self.farm_manager_token}",
            format="json",
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_flock_movement_as_assistant_farm_manager_permission_denied(self):
        """
        Test delete flock movement records by an assistant farm manager (should be denied).
        """

        serializer = FlockMovementSerializer(data=self.flock_movement_data)
        serializer.is_valid()
        flock_movement = serializer.save()

        response = self.client.delete(
            reverse("poultry:flock-movements-detail", kwargs={"pk": flock_movement.id}),
            HTTP_AUTHORIZATION=f"Token {self.asst_farm_manager_token}",
            format="json",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_flock_movement_as_team_leader_permission_denied(self):
        """
        Test delete flock movement records by a team leader (should be denied).
        """

        serializer = FlockMovementSerializer(data=self.flock_movement_data)
        serializer.is_valid()
        flock_movement = serializer.save()

        response = self.client.delete(
            reverse("poultry:flock-movements-detail", kwargs={"pk": flock_movement.id}),
            HTTP_AUTHORIZATION=f"Token {self.team_leader_token}",
            format="json",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_flock_movement_a_farm_worker_permission_denied(self):
        """
        Test delete flock movement records by a farm worker (should be denied).
        """

        serializer = FlockMovementSerializer(data=self.flock_movement_data)
        serializer.is_valid()
        flock_movement = serializer.save()

        response = self.client.delete(
            reverse("poultry:flock-movements-detail", kwargs={"pk": flock_movement.id}),
            HTTP_AUTHORIZATION=f"Token {self.farm_worker_token}",
            format="json",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_flock_movement_a_regular_user_permission_denied(self):
        """
        Test delete flock movement records by a regular user(should be denied).
        """

        serializer = FlockMovementSerializer(data=self.flock_movement_data)
        serializer.is_valid()
        flock_movement = serializer.save()

        response = self.client.delete(
            reverse("poultry:flock-movements-detail", kwargs={"pk": flock_movement.id}),
            HTTP_AUTHORIZATION=f"Token {self.regular_user_token}",
            format="json",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_flock_movement_without_authentication(self):
        """
        Test delete flock movement records without authentication. (should be denied).
        """

        serializer = FlockMovementSerializer(data=self.flock_movement_data)
        serializer.is_valid()
        flock_movement = serializer.save()

        response = self.client.delete(
            reverse("poultry:flock-movements-detail", kwargs={"pk": flock_movement.id}),
            format="json",
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestFlockInspectionViewSet:
    @pytest.fixture(autouse=True)
    def setup(self, setup_users, setup_flock_inspection_data):
        self.client = setup_users["client"]

        self.regular_user_token = setup_users["regular_user_token"]
        self.farm_owner_token = setup_users["farm_owner_token"]
        self.farm_manager_token = setup_users["farm_manager_token"]
        self.asst_farm_manager_token = setup_users["asst_farm_manager_token"]
        self.team_leader_token = setup_users["team_leader_token"]
        self.farm_worker_token = setup_users["farm_worker_token"]

        self.flock_inspection_data = setup_flock_inspection_data[
            "flock_inspection_data"
        ]

    def test_add_flock_inspection_as_farm_owner(self):
        """
        Test add flock inspection record by a farm owner.
        """
        response = self.client.post(
            reverse("poultry:flock-inspection-records-list"),
            data=self.flock_inspection_data,
            HTTP_AUTHORIZATION=f"Token {self.farm_owner_token}",
            format="json",
        )
        assert response.status_code == status.HTTP_201_CREATED

    def test_add_flock_movement_as_farm_manager(self):
        """
        Test add flock inspection data by a farm manager.
        """
        response = self.client.post(
            reverse("poultry:flock-inspection-records-list"),
            data=self.flock_inspection_data,
            HTTP_AUTHORIZATION=f"Token {self.farm_manager_token}",
            format="json",
        )
        assert response.status_code == status.HTTP_201_CREATED

    def test_add_flock_movement_as_an_assistant_farm_manager(self):
        """
        Test add flock inspection data by an assistant farm manager.
        """
        response = self.client.post(
            reverse("poultry:flock-inspection-records-list"),
            data=self.flock_inspection_data,
            HTTP_AUTHORIZATION=f"Token {self.asst_farm_manager_token}",
            format="json",
        )
        assert response.status_code == status.HTTP_201_CREATED

    def test_add_flock_movement_as_team_leader(self):
        """
        Test add flock inspection data by a team leader.
        """
        response = self.client.post(
            reverse("poultry:flock-inspection-records-list"),
            data=self.flock_inspection_data,
            HTTP_AUTHORIZATION=f"Token {self.team_leader_token}",
            format="json",
        )
        assert response.status_code == status.HTTP_201_CREATED

    def test_add_flock_movement_as_farm_worker(self):
        """
        Test add flock inspection data by a farm worker.
        """
        response = self.client.post(
            reverse("poultry:flock-inspection-records-list"),
            data=self.flock_inspection_data,
            HTTP_AUTHORIZATION=f"Token {self.farm_worker_token}",
            format="json",
        )
        assert response.status_code == status.HTTP_201_CREATED

    def test_add_flock_movement_as_regular_user(self):
        """
        Test add flock inspection data by a regular user.
        """
        response = self.client.post(
            reverse("poultry:flock-inspection-records-list"),
            data=self.flock_inspection_data,
            HTTP_AUTHORIZATION=f"Token {self.regular_user_token}",
            format="json",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_add_flock_movement_without_authentication(self):
        """
        Test add flock inspection data without authentication.
        """
        response = self.client.post(
            reverse("poultry:flock-inspection-records-list"),
            data=self.flock_inspection_data,
            format="json",
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_flock_movement_as_farm_owner(self):
        """
        Test list flock inspection records by a farm owner.
        """
        response = self.client.get(
            reverse("poultry:flock-inspection-records-list"),
            HTTP_AUTHORIZATION=f"Token {self.farm_owner_token}",
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK

    def test_list_flock_movement_as_farm_manager(self):
        """
        Test list flock inspection records by a farm manager.
        """
        response = self.client.get(
            reverse("poultry:flock-inspection-records-list"),
            HTTP_AUTHORIZATION=f"Token {self.farm_manager_token}",
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK

    def test_list_flock_movement_as_an_assistant_farm_manager(self):
        """
        Test list flock inspection records by an assistant farm manager.
        """
        response = self.client.get(
            reverse("poultry:flock-inspection-records-list"),
            HTTP_AUTHORIZATION=f"Token {self.asst_farm_manager_token}",
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK

    def test_list_flock_movement_as_team_leader(self):
        """
        Test list flock inspection records by a team leader.
        """
        response = self.client.get(
            reverse("poultry:flock-inspection-records-list"),
            HTTP_AUTHORIZATION=f"Token {self.team_leader_token}",
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK

    def test_list_flock_movement_as_farm_worker(self):
        """
        Test list flock inspection data by a farm worker.
        """
        response = self.client.get(
            reverse("poultry:flock-inspection-records-list"),
            HTTP_AUTHORIZATION=f"Token {self.farm_worker_token}",
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK

    def test_list_flock_movement_as_regular_user_permission_denied(self):
        """
        Test list flock inspection data by a regular user (permission denied).
        """
        response = self.client.get(
            reverse("poultry:flock-inspection-records-list"),
            HTTP_AUTHORIZATION=f"Token {self.regular_user_token}",
            format="json",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_list_flock_movement_without_authentication(self):
        """
        Test list flock inspection data without authentication. (permission denied).
        """
        response = self.client.get(
            reverse("poultry:flock-inspection-records-list"), format="json"
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_flock_movement_as_farm_owner(self):
        """
        Test update flock inspection records by a farm owner.
        """
        serializer = FlockInspectionRecordSerializer(data=self.flock_inspection_data)
        serializer.is_valid()
        flock_inspection = serializer.save()

        flock_inspection_update_data = {"number_of_dead_birds": 10}

        response = self.client.patch(
            reverse(
                "poultry:flock-inspection-records-detail",
                kwargs={"pk": flock_inspection.id},
            ),
            data=flock_inspection_update_data,
            HTTP_AUTHORIZATION=f"Token {self.farm_owner_token}",
            format="json",
        )
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_delete_flock_breed_information_as_farm_owner(self):
        """
        Test delete flock inspection records by a farm owner.
        """

        serializer = FlockInspectionRecordSerializer(data=self.flock_inspection_data)
        serializer.is_valid()
        flock_inspection = serializer.save()

        response = self.client.delete(
            reverse(
                "poultry:flock-inspection-records-detail",
                kwargs={"pk": flock_inspection.id},
            ),
            HTTP_AUTHORIZATION=f"Token {self.farm_owner_token}",
            format="json",
        )
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.django_db
class TestFlockBreedInformationViewSet:
    @pytest.fixture(autouse=True)
    def setup(self, setup_users, setup_flock_breed_information_data):
        self.client = setup_users["client"]

        self.regular_user_token = setup_users["regular_user_token"]
        self.farm_owner_token = setup_users["farm_owner_token"]
        self.farm_manager_token = setup_users["farm_manager_token"]
        self.asst_farm_manager_token = setup_users["asst_farm_manager_token"]
        self.team_leader_token = setup_users["team_leader_token"]
        self.farm_worker_token = setup_users["farm_worker_token"]

        self.flock_breed_information_data = setup_flock_breed_information_data[
            "flock_breed_information_data"
        ]

    def test_add_flock_breed_information_as_farm_owner(self):
        """
        Test add flock breed information record by a farm owner.
        """
        response = self.client.post(
            reverse("poultry:flock-breed-information-list"),
            data=self.flock_breed_information_data,
            HTTP_AUTHORIZATION=f"Token {self.farm_owner_token}",
            format="json",
        )
        assert response.status_code == status.HTTP_201_CREATED

    def test_add_flock_breed_information_as_farm_manager(self):
        """
        Test add flock breed information data by a farm manager.
        """
        response = self.client.post(
            reverse("poultry:flock-breed-information-list"),
            data=self.flock_breed_information_data,
            HTTP_AUTHORIZATION=f"Token {self.farm_manager_token}",
            format="json",
        )
        assert response.status_code == status.HTTP_201_CREATED

    def test_add_flock_breed_information_as_an_assistant_farm_manager_permission_denied(
        self,
    ):
        """
        Test add flock breed information data by an assistant farm manager (permission denied).
        """
        response = self.client.post(
            reverse("poultry:flock-breed-information-list"),
            data=self.flock_breed_information_data,
            HTTP_AUTHORIZATION=f"Token {self.asst_farm_manager_token}",
            format="json",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_add_flock_breed_information_as_team_leader_permission_denied(self):
        """
        Test add flock breed information data by a team leader (permission denied).
        """
        response = self.client.post(
            reverse("poultry:flock-breed-information-list"),
            data=self.flock_breed_information_data,
            HTTP_AUTHORIZATION=f"Token {self.team_leader_token}",
            format="json",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_add_flock_breed_information_as_farm_worker_permission_denied(self):
        """
        Test add flock breed information data by a farm worker(permission denied).
        """
        response = self.client.post(
            reverse("poultry:flock-breed-information-list"),
            data=self.flock_breed_information_data,
            HTTP_AUTHORIZATION=f"Token {self.farm_worker_token}",
            format="json",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_add_flock_breed_information_as_regular_user_permission_denied(self):
        """
        Test add flock breed information data by a regular user (permission denied).
        """
        response = self.client.post(
            reverse("poultry:flock-breed-information-list"),
            data=self.flock_breed_information_data,
            HTTP_AUTHORIZATION=f"Token {self.regular_user_token}",
            format="json",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_add_flock_breed_information_without_authentication(self):
        """
        Test add flock breed information data without authentication (permission denied).
        """
        response = self.client.post(
            reverse("poultry:flock-breed-information-list"),
            data=self.flock_breed_information_data,
            format="json",
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_flock_breed_information_as_farm_owner(self):
        """
        Test list flock breed information records by a farm owner.
        """
        response = self.client.get(
            reverse("poultry:flock-breed-information-list"),
            HTTP_AUTHORIZATION=f"Token {self.farm_owner_token}",
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK

    def test_list_flock_breed_information_as_farm_manager(self):
        """
        Test list flock breed information records by a farm manager.
        """
        response = self.client.get(
            reverse("poultry:flock-breed-information-list"),
            HTTP_AUTHORIZATION=f"Token {self.farm_manager_token}",
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK

    def test_list_flock_breed_information_as_an_assistant_farm_manager_permission_denied(
        self,
    ):
        """
        Test list flock breed information records by an assistant farm manager (permission denied).
        """
        response = self.client.get(
            reverse("poultry:flock-breed-information-list"),
            HTTP_AUTHORIZATION=f"Token {self.asst_farm_manager_token}",
            format="json",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_list_flock_breed_information_as_team_leader_permission_denied(self):
        """
        Test list flock breed information records by a team leader (permission denied).
        """
        response = self.client.get(
            reverse("poultry:flock-breed-information-list"),
            HTTP_AUTHORIZATION=f"Token {self.team_leader_token}",
            format="json",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_list_flock_breed_information_as_farm_worker_permission_denied(self):
        """
        Test list flock breed information data by a farm worker(permission denied).
        """
        response = self.client.get(
            reverse("poultry:flock-breed-information-list"),
            HTTP_AUTHORIZATION=f"Token {self.farm_worker_token}",
            format="json",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_list_flock_breed_information_as_regular_user_permission_denied(self):
        """
        Test list flock breed information data by a regular user (permission denied).
        """
        response = self.client.get(
            reverse("poultry:flock-breed-information-list"),
            HTTP_AUTHORIZATION=f"Token {self.regular_user_token}",
            format="json",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_list_flock_breed_information_without_authentication(self):
        """
        Test list flock breed information data without authentication. (permission denied).
        """
        response = self.client.get(
            reverse("poultry:flock-breed-information-list"), format="json"
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_flock_breed_information_as_farm_owner(self):
        """
        Test update flock breed information records by a farm owner.
        """

        serializer = FlockBreedInformationSerializer(
            data=self.flock_breed_information_data
        )
        serializer.is_valid()
        flock_breed_information = serializer.save()
        flock_breed_information_update_data = {"average_mature_weight_in_kgs": 2.7}

        response = self.client.patch(
            reverse(
                "poultry:flock-breed-information-detail",
                kwargs={"pk": flock_breed_information.id},
            ),
            data=flock_breed_information_update_data,
            HTTP_AUTHORIZATION=f"Token {self.farm_owner_token}",
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK

    def test_update_flock_breed_information_as_farm_manager(self):
        """
        Test update flock breed information records by a farm manager.
        """

        serializer = FlockBreedInformationSerializer(
            data=self.flock_breed_information_data
        )
        serializer.is_valid()
        flock_breed_information = serializer.save()
        flock_breed_information_update_data = {"average_mature_weight_in_kgs": 2.7}

        response = self.client.patch(
            reverse(
                "poultry:flock-breed-information-detail",
                kwargs={"pk": flock_breed_information.id},
            ),
            data=flock_breed_information_update_data,
            HTTP_AUTHORIZATION=f"Token {self.farm_manager_token}",
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK

    def test_update_flock_breed_information_as_assistant_farm_manager_permission_denied(
        self,
    ):
        """
        Test update flock breed information records by an assistant farm manager (should be denied).
        """

        serializer = FlockBreedInformationSerializer(
            data=self.flock_breed_information_data
        )
        serializer.is_valid()
        flock_breed_information = serializer.save()
        flock_breed_information_update_data = {"average_mature_weight_in_kgs": 2.7}

        response = self.client.patch(
            reverse(
                "poultry:flock-breed-information-detail",
                kwargs={"pk": flock_breed_information.id},
            ),
            data=flock_breed_information_update_data,
            HTTP_AUTHORIZATION=f"Token {self.asst_farm_manager_token}",
            format="json",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_flock_breed_information_as_team_leader_permission_denied(self):
        """
        Test update flock breed information records by a team leader (should be denied).
        """

        serializer = FlockBreedInformationSerializer(
            data=self.flock_breed_information_data
        )
        serializer.is_valid()
        flock_breed_information = serializer.save()
        flock_breed_information_update_data = {"average_mature_weight_in_kgs": 2.7}

        response = self.client.patch(
            reverse(
                "poultry:flock-breed-information-detail",
                kwargs={"pk": flock_breed_information.id},
            ),
            data=flock_breed_information_update_data,
            HTTP_AUTHORIZATION=f"Token {self.team_leader_token}",
            format="json",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_flock_breed_information_a_farm_worker_permission_denied(self):
        """
        Test update flock breed information records by a farm worker (should be denied).
        """

        serializer = FlockBreedInformationSerializer(
            data=self.flock_breed_information_data
        )
        serializer.is_valid()
        flock_breed_information = serializer.save()
        flock_breed_information_update_data = {"average_mature_weight_in_kgs": 2.7}

        response = self.client.patch(
            reverse(
                "poultry:flock-breed-information-detail",
                kwargs={"pk": flock_breed_information.id},
            ),
            data=flock_breed_information_update_data,
            HTTP_AUTHORIZATION=f"Token {self.farm_worker_token}",
            format="json",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_flock_breed_information_a_regular_user_permission_denied(self):
        """
        Test update flock breed information records by a regular user(should be denied).
        """

        serializer = FlockBreedInformationSerializer(
            data=self.flock_breed_information_data
        )
        serializer.is_valid()
        flock_breed_information = serializer.save()
        flock_breed_information_update_data = {"average_mature_weight_in_kgs": 2.7}

        response = self.client.patch(
            reverse(
                "poultry:flock-breed-information-detail",
                kwargs={"pk": flock_breed_information.id},
            ),
            data=flock_breed_information_update_data,
            HTTP_AUTHORIZATION=f"Token {self.regular_user_token}",
            format="json",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_flock_breed_information_without_authentication(self):
        """
        Test update flock breed information records without authentication. (should be denied).
        """

        serializer = FlockBreedInformationSerializer(
            data=self.flock_breed_information_data
        )
        serializer.is_valid()
        flock_breed_information = serializer.save()
        flock_breed_information_update_data = {
            "to_structure": self.flock_breed_information_data
        }

        response = self.client.patch(
            reverse(
                "poultry:flock-breed-information-detail",
                kwargs={"pk": flock_breed_information.id},
            ),
            data=flock_breed_information_update_data,
            format="json",
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_flock_breed_information_as_farm_owner(self):
        """
        Test delete flock breed information records by a farm owner.
        """

        serializer = FlockBreedInformationSerializer(
            data=self.flock_breed_information_data
        )
        serializer.is_valid()
        flock_breed_information = serializer.save()

        response = self.client.delete(
            reverse(
                "poultry:flock-breed-information-detail",
                kwargs={"pk": flock_breed_information.id},
            ),
            HTTP_AUTHORIZATION=f"Token {self.farm_owner_token}",
            format="json",
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_flock_breed_information_as_farm_manager(self):
        """
        Test delete flock breed information records by a farm manager.
        """

        serializer = FlockBreedInformationSerializer(
            data=self.flock_breed_information_data
        )
        serializer.is_valid()
        flock_breed_information = serializer.save()

        response = self.client.delete(
            reverse(
                "poultry:flock-breed-information-detail",
                kwargs={"pk": flock_breed_information.id},
            ),
            HTTP_AUTHORIZATION=f"Token {self.farm_manager_token}",
            format="json",
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_flock_breed_information_as_assistant_farm_manager_permission_denied(
        self,
    ):
        """
        Test delete flock breed information records by an assistant farm manager (should be denied).
        """

        serializer = FlockBreedInformationSerializer(
            data=self.flock_breed_information_data
        )
        serializer.is_valid()
        flock_breed_information = serializer.save()

        response = self.client.delete(
            reverse(
                "poultry:flock-breed-information-detail",
                kwargs={"pk": flock_breed_information.id},
            ),
            HTTP_AUTHORIZATION=f"Token {self.asst_farm_manager_token}",
            format="json",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_flock_breed_information_as_team_leader_permission_denied(self):
        """
        Test delete flock breed information records by a team leader (should be denied).
        """

        serializer = FlockBreedInformationSerializer(
            data=self.flock_breed_information_data
        )
        serializer.is_valid()
        flock_breed_information = serializer.save()

        response = self.client.delete(
            reverse(
                "poultry:flock-breed-information-detail",
                kwargs={"pk": flock_breed_information.id},
            ),
            HTTP_AUTHORIZATION=f"Token {self.team_leader_token}",
            format="json",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_flock_breed_information_a_farm_worker_permission_denied(self):
        """
        Test delete flock breed information records by a farm worker (should be denied).
        """

        serializer = FlockBreedInformationSerializer(
            data=self.flock_breed_information_data
        )
        serializer.is_valid()
        flock_breed_information = serializer.save()

        response = self.client.delete(
            reverse(
                "poultry:flock-breed-information-detail",
                kwargs={"pk": flock_breed_information.id},
            ),
            HTTP_AUTHORIZATION=f"Token {self.farm_worker_token}",
            format="json",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_flock_breed_information_a_regular_user_permission_denied(self):
        """
        Test delete flock breed information records by a regular user(should be denied).
        """

        serializer = FlockBreedInformationSerializer(
            data=self.flock_breed_information_data
        )
        serializer.is_valid()
        flock_breed_information = serializer.save()

        response = self.client.delete(
            reverse(
                "poultry:flock-breed-information-detail",
                kwargs={"pk": flock_breed_information.id},
            ),
            HTTP_AUTHORIZATION=f"Token {self.regular_user_token}",
            format="json",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_flock_breed_information_without_authentication(self):
        """
        Test delete flock breed information records without authentication. (should be denied).
        """

        serializer = FlockBreedInformationSerializer(
            data=self.flock_breed_information_data
        )
        serializer.is_valid()
        flock_breed_information = serializer.save()

        response = self.client.delete(
            reverse(
                "poultry:flock-breed-information-detail",
                kwargs={"pk": flock_breed_information.id},
            ),
            format="json",
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestEggCollectionViewSet:
    @pytest.fixture(autouse=True)
    def setup(self, setup_users, setup_egg_collection_data):
        self.client = setup_users["client"]

        self.regular_user_token = setup_users["regular_user_token"]
        self.farm_owner_token = setup_users["farm_owner_token"]
        self.farm_manager_token = setup_users["farm_manager_token"]
        self.asst_farm_manager_token = setup_users["asst_farm_manager_token"]
        self.team_leader_token = setup_users["team_leader_token"]
        self.farm_worker_token = setup_users["farm_worker_token"]

        self.egg_collection_data = setup_egg_collection_data["egg_collection_data"]

    def test_add_egg_collection_as_farm_owner(self):
        """
        Test adding egg collection record by a farm owner.
        """
        response = self.client.post(
            reverse("poultry:egg-collection-list"),
            data=self.egg_collection_data,
            HTTP_AUTHORIZATION=f"Token {self.farm_owner_token}",
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert EggCollection.objects.filter(
            flock=self.egg_collection_data["flock"]
        ).exists()

    def test_add_egg_collection_as_farm_manager(self):
        """
        Test adding egg collection record by a farm manager
        """

        response = self.client.post(
            reverse("poultry:egg-collection-list"),
            data=self.egg_collection_data,
            HTTP_AUTHORIZATION=f"Token {self.farm_manager_token}",
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert EggCollection.objects.filter(
            flock=self.egg_collection_data["flock"]
        ).exists()

    def test_add_egg_collection_as_asst_farm_manager(self):
        """
        Test adding egg collection record by an assistant farm manager.
        """

        response = self.client.post(
            reverse("poultry:egg-collection-list"),
            data=self.egg_collection_data,
            HTTP_AUTHORIZATION=f"Token {self.asst_farm_manager_token}",
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert EggCollection.objects.filter(
            flock=self.egg_collection_data["flock"]
        ).exists()

    def test_add_egg_collection_as_team_leader(self):
        """
        Test adding egg collection record by a team leader.
        """

        response = self.client.post(
            reverse("poultry:egg-collection-list"),
            data=self.egg_collection_data,
            HTTP_AUTHORIZATION=f"Token {self.team_leader_token}",
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert EggCollection.objects.filter(
            flock=self.egg_collection_data["flock"]
        ).exists()

    def test_add_egg_collection_as_farm_worker(self):
        """
        Test adding egg collection record by a farm worker.
        """

        response = self.client.post(
            reverse("poultry:egg-collection-list"),
            data=self.egg_collection_data,
            HTTP_AUTHORIZATION=f"Token {self.farm_worker_token}",
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert EggCollection.objects.filter(
            flock=self.egg_collection_data["flock"]
        ).exists()

    def test_add_egg_collection_as_regular_user_permission_denied(self):
        """
        Test adding egg collection record by a regular user (should be denied).
        """

        response = self.client.post(
            reverse("poultry:egg-collection-list"),
            data=self.egg_collection_data,
            HTTP_AUTHORIZATION=f"Token {self.regular_user_token}",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not EggCollection.objects.filter(
            flock=self.egg_collection_data["flock"]
        ).exists()

    def test_add_egg_collection_without_authentication(self):
        """
        Test adding egg collection record without authentication (should be denied).
        """

        response = self.client.post(
            reverse("poultry:egg-collection-list"), self.egg_collection_data
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert not EggCollection.objects.filter(
            flock=self.egg_collection_data["flock"]
        ).exists()

    def test_retrieve_egg_collection_as_farm_owner(self):
        """
        Test retrieving egg collection by a farm owner.
        """
        response = self.client.get(
            reverse("poultry:egg-collection-list"),
            HTTP_AUTHORIZATION=f"Token {self.farm_owner_token}",
        )
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_egg_collection_as_farm_manager(self):
        """
        Test retrieving egg collection by a farm manager.
        """
        response = self.client.get(
            reverse("poultry:egg-collection-list"),
            HTTP_AUTHORIZATION=f"Token {self.farm_manager_token}",
        )
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_egg_collection_as_asst_farm_manager_permission_denied(self):
        """
        Test retrieving egg collection by an assistant farm manager.
        """
        response = self.client.get(
            reverse("poultry:egg-collection-list"),
            HTTP_AUTHORIZATION=f"Token {self.asst_farm_manager_token}",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_retrieve_egg_collection_as_team_leader_permission_denied(self):
        """
        Test retrieving egg collection by a team leader (permission denied).
        """
        response = self.client.get(
            reverse("poultry:egg-collection-list"),
            HTTP_AUTHORIZATION=f"Token {self.team_leader_token}",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_retrieve_egg_collection_as_farm_worker_permission_denied(self):
        """
        Test retrieving egg collection by a farm worker (permission denied).
        """
        response = self.client.get(
            reverse("poultry:egg-collection-list"),
            HTTP_AUTHORIZATION=f"Token {self.farm_worker_token}",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_retrieve_egg_collection_as_regular_user_permission_denied(self):
        """
        Test retrieving egg collection by a regular user (should be denied).
        """
        response = self.client.get(
            reverse("poultry:egg-collection-list"),
            HTTP_AUTHORIZATION=f"Token {self.regular_user_token}",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_retrieve_egg_collection_without_authentication(self):
        """
        Test retrieving egg collection without authentication (should be denied).
        """
        url = reverse("poultry:egg-collection-list")
        response = self.client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_egg_collection_permission_denied(self):
        """
        Test updating egg collection (should be denied).
        """
        serializer = EggCollectionSerializer(data=self.egg_collection_data)
        serializer.is_valid()
        egg_collection = serializer.save()

        url = reverse("poultry:egg-collection-detail", kwargs={"pk": egg_collection.id})
        egg_collection_update_data = {"collected_eggs": 79}
        response = self.client.patch(
            url,
            data=egg_collection_update_data,
            HTTP_AUTHORIZATION=f"Token {self.farm_owner_token}",
        )
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_delete_egg_collection_as_farm_owner(self):
        """
        Test deleting egg collection by a farm owner.
        """
        serializer = EggCollectionSerializer(data=self.egg_collection_data)
        serializer.is_valid()
        egg_collection = serializer.save()

        url = reverse("poultry:egg-collection-detail", kwargs={"pk": egg_collection.id})
        response = self.client.delete(
            url,
            HTTP_AUTHORIZATION=f"Token {self.farm_owner_token}",
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not EggCollection.objects.filter(id=egg_collection.id).exists()

    def test_delete_egg_collection_as_farm_manager(self):
        """
        Test deleting egg collection by a farm manager.
        """
        serializer = EggCollectionSerializer(data=self.egg_collection_data)
        serializer.is_valid()
        egg_collection = serializer.save()

        url = reverse("poultry:egg-collection-detail", kwargs={"pk": egg_collection.id})
        response = self.client.delete(
            url,
            HTTP_AUTHORIZATION=f"Token {self.farm_manager_token}",
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not EggCollection.objects.filter(id=egg_collection.id).exists()

    def test_delete_egg_collection_as_asst_farm_manager_permission_denied(self):
        """
        Test deleting egg collection by an assistant farm manager (should be denied).
        """
        serializer = EggCollectionSerializer(data=self.egg_collection_data)
        serializer.is_valid()
        egg_collection = serializer.save()

        url = reverse("poultry:egg-collection-detail", kwargs={"pk": egg_collection.id})
        response = self.client.delete(
            url,
            HTTP_AUTHORIZATION=f"Token {self.asst_farm_manager_token}",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert EggCollection.objects.filter(id=egg_collection.id).exists()

    def test_delete_egg_collection_as_team_leader_permission_denied(self):
        """
        Test deleting egg collection by a team leader (should be denied).
        """
        serializer = EggCollectionSerializer(data=self.egg_collection_data)
        serializer.is_valid()
        egg_collection = serializer.save()

        url = reverse("poultry:egg-collection-detail", kwargs={"pk": egg_collection.id})
        response = self.client.delete(
            url,
            HTTP_AUTHORIZATION=f"Token {self.team_leader_token}",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert EggCollection.objects.filter(id=egg_collection.id).exists()

    def test_delete_egg_collection_as_farm_worker_permission_denied(self):
        """
        Test deleting egg collection by a farm worker (should be denied).
        """
        serializer = EggCollectionSerializer(data=self.egg_collection_data)
        serializer.is_valid()
        egg_collection = serializer.save()

        url = reverse("poultry:egg-collection-detail", kwargs={"pk": egg_collection.id})
        response = self.client.delete(
            url,
            HTTP_AUTHORIZATION=f"Token {self.farm_worker_token}",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert EggCollection.objects.filter(id=egg_collection.id).exists()

    def test_delete_egg_collection_as_regular_user_permission_denied(self):
        """
        Test delete egg collection as a regular user (permission denied)
        """
        serializer = EggCollectionSerializer(data=self.egg_collection_data)
        serializer.is_valid()
        egg_collection = serializer.save()

        url = reverse("poultry:egg-collection-detail", kwargs={"pk": egg_collection.id})
        response = self.client.delete(
            url,
            HTTP_AUTHORIZATION=f"Token {self.regular_user_token}",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert EggCollection.objects.filter(id=egg_collection.id).exists()

    def test_delete_egg_collection_without_authentication(self):
        """
        Test delete egg collection by unauthorized request
        """
        serializer = EggCollectionSerializer(data=self.egg_collection_data)
        serializer.is_valid()
        egg_collection = serializer.save()

        url = reverse("poultry:egg-collection-detail", kwargs={"pk": egg_collection.id})
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert EggCollection.objects.filter(id=egg_collection.id).exists()
