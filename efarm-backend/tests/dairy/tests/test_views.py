import pytest
from django.urls import reverse

from dairy.views import *


@pytest.mark.django_db
class TestCowBreedViewSet:
    @pytest.fixture(autouse=True)
    def setup(self, setup_users):
        self.client = setup_users['client']

        self.regular_user_id = setup_users['regular_user_id']
        self.regular_user_token = setup_users['regular_user_token']
        self.regular_user_username = setup_users['regular_user_username']

        self.farm_owner_token = setup_users['farm_owner_token']
        self.farm_owner_user_id = setup_users['farm_owner_user_id']
        self.farm_owner_user_username = setup_users['farm_owner_user_username']

        self.farm_manager_token = setup_users['farm_manager_token']
        self.farm_manager_user_id = setup_users['farm_manager_user_id']
        self.farm_manager_user_username = setup_users['farm_manager_user_username']

        self.asst_farm_manager_token = setup_users['asst_farm_manager_token']
        self.asst_farm_manager_user_id = setup_users['asst_farm_manager_user_id']
        self.asst_farm_manager_user_username = setup_users['asst_farm_manager_user_username']

        self.team_leader_token = setup_users['team_leader_token']
        self.team_leader_user_id = setup_users['team_leader_user_id']
        self.team_leader_user_username = setup_users['team_leader_user_username']

        self.farm_worker_token = setup_users['farm_worker_token']
        self.farm_worker_user_id = setup_users['farm_worker_user_id']
        self.farm_worker_user_username = setup_users['farm_worker_user_username']

    def test_create_cow_breed_as_farm_owner(self):
        # Farm owners should be able to create cow breeds
        url = reverse('dairy:cow-breeds-list')
        cow_breed_data = {'name': CowBreedChoices.GUERNSEY}
        headers = {'Authorization': f'Token {self.farm_owner_token}'}
        response = self.client.post(url, data=cow_breed_data, headers=headers)
        assert response.status_code == status.HTTP_201_CREATED
        assert CowBreed.objects.filter(name=cow_breed_data['name']).exists()

    def test_create_cow_breed_as_farm_manager(self):
        # Farm managers should not be able to create cow breeds
        url = reverse('dairy:cow-breeds-list')
        cow_breed_data = {'name': CowBreedChoices.GUERNSEY}
        headers = {'Authorization': f'Token {self.farm_manager_token}'}
        response = self.client.post(url, cow_breed_data, headers=headers)
        assert response.status_code == status.HTTP_201_CREATED
        assert CowBreed.objects.filter(name=cow_breed_data['name']).exists()

    def test_create_cow_breed_as_regular_user_permission_denied(self):
        # Regular users should not be able to create cow breeds
        url = reverse('dairy:cow-breeds-list')
        cow_breed_data = {'name': CowBreedChoices.AYRSHIRE}
        headers = {'Authorization': f'Token {self.regular_user_token}'}
        response = self.client.post(url, cow_breed_data, headers=headers)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not CowBreed.objects.filter(name=cow_breed_data['name']).exists()

    def test_create_cow_breed_as_farm_worker_permission_denied(self):
        # Regular users should not be able to create cow breeds
        url = reverse('dairy:cow-breeds-list')
        cow_breed_data = {'name': CowBreedChoices.AYRSHIRE}
        headers = {'Authorization': f'Token {self.farm_worker_token}'}
        response = self.client.post(url, cow_breed_data, headers=headers)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not CowBreed.objects.filter(name=cow_breed_data['name']).exists()

    def test_retrieve_cow_breeds_as_farm_owner(self):
        # Farm owners should be able to retrieve cow breeds
        url = reverse('dairy:cow-breeds-list')
        CowBreed.objects.create(name=CowBreedChoices.AYRSHIRE)
        headers = {'Authorization': f'Token {self.farm_owner_token}'}
        response = self.client.get(url, headers=headers)
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_cow_breeds_as_farm_manager(self):
        # Farm managers should be able to retrieve cow breeds
        url = reverse('dairy:cow-breeds-list')
        headers = {'Authorization': f'Token {self.farm_manager_token}'}
        response = self.client.get(url, headers=headers)
        assert response.status_code == status.HTTP_200_OK
        # Ensure that the response contains the expected data

    def test_retrieve_cow_breeds_as_regular_user_permission_denied(self):
        # Regular users should be able to retrieve cow breeds
        url = reverse('dairy:cow-breeds-list')
        headers = {'Authorization': f'Token {self.regular_user_token}'}
        response = self.client.get(url, headers=headers)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        # Ensure that the response contains the expected data

    def test_update_cow_breed_permission_denied(self):
        # Any user (including farm owners and managers) should not be able to update cow breeds
        cow_breed = CowBreed.objects.create(name=CowBreedChoices.FRIESIAN)
        url = reverse('dairy:cow-breeds-detail', kwargs={'pk': cow_breed.id})
        cow_breed_update_data = {'name': CowBreedChoices.AYRSHIRE}
        headers = {'Authorization': f'Token {self.farm_owner_token}'}
        response = self.client.put(url, cow_breed_update_data, headers=headers)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        # Ensure that the cow breed name remains unchanged

    def test_delete_cow_breed_as_farm_owner(self):
        # Farm owners should be able to delete cow breeds
        cow_breed = CowBreed.objects.create(name=CowBreedChoices.FRIESIAN)
        url = reverse('dairy:cow-breeds-detail', kwargs={'pk': cow_breed.id})
        headers = {'Authorization': f'Token {self.farm_owner_token}'}
        response = self.client.delete(url, headers=headers)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not CowBreed.objects.filter(id=cow_breed.id).exists()

    def test_delete_cow_breed_as_farm_manager(self):
        # Farm managers should not be able to delete cow breeds
        cow_breed = CowBreed.objects.create(name=CowBreedChoices.SAHIWAL)
        url = reverse('dairy:cow-breeds-detail', kwargs={'pk': cow_breed.id})
        headers = {'Authorization': f'Token {self.farm_manager_token}'}
        response = self.client.delete(url, headers=headers)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not CowBreed.objects.filter(id=cow_breed.id).exists()

    def test_delete_cow_breed_as_regular_user_permission_denied(self):
        # Regular users should not be able to delete cow breeds
        cow_breed = CowBreed.objects.create(name=CowBreedChoices.SAHIWAL)
        url = reverse('dairy:cow-breeds-detail', kwargs={'pk': cow_breed.id})
        headers = {'Authorization': f'Token {self.regular_user_token}'}
        response = self.client.delete(url, headers=headers)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert CowBreed.objects.filter(id=cow_breed.id).exists()

    def test_delete_cow_breed_as_farm_worker_permission_denied(self):
        # Regular users should not be able to delete cow breeds
        cow_breed = CowBreed.objects.create(name=CowBreedChoices.CROSSBREED)
        url = reverse('dairy:cow-breeds-detail', kwargs={'pk': cow_breed.id})
        headers = {'Authorization': f'Token {self.farm_worker_token}'}
        response = self.client.delete(url, headers=headers)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert CowBreed.objects.filter(id=cow_breed.id).exists()

    def test_filter_cow_breeds_by_name(self):
        # Filter cow breeds by name (e.g., get all breeds with name 'Jersey')
        CowBreed.objects.create(name=CowBreedChoices.JERSEY)
        CowBreed.objects.create(name=CowBreedChoices.CROSSBREED)
        url = reverse('dairy:cow-breeds-list')
        url += f'?name={CowBreedChoices.JERSEY}'  # Append the name parameter to the URL directly
        headers = {'Authorization': f'Token {self.farm_owner_token}'}
        response = self.client.get(url, headers=headers)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['name'] == CowBreedChoices.JERSEY

    def test_filter_cow_breeds_by_partial_name(self):
        # Filter cow breeds by partial name (e.g., get breeds with names containing 'ey')
        CowBreed.objects.create(name=CowBreedChoices.JERSEY)
        CowBreed.objects.create(name=CowBreedChoices.GUERNSEY)
        url = reverse('dairy:cow-breeds-list')
        url += '?name=ey'
        headers = {'Authorization': f'Token {self.asst_farm_manager_token}'}
        response = self.client.get(url, headers=headers)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        assert [cow_breed['name'] for cow_breed in response.data] == [CowBreedChoices.JERSEY,
                                                                      CowBreedChoices.GUERNSEY]

    def test_order_cow_breeds_by_multiple_fields(self):
        # Order cow breeds by multiple fields (e.g., name in descending order, id in ascending order)
        CowBreed.objects.create(name=CowBreedChoices.JERSEY)
        CowBreed.objects.create(name=CowBreedChoices.GUERNSEY)
        CowBreed.objects.create(name=CowBreedChoices.CROSSBREED)
        CowBreed.objects.create(name=CowBreedChoices.SAHIWAL)
        CowBreed.objects.create(name=CowBreedChoices.AYRSHIRE)
        CowBreed.objects.create(name=CowBreedChoices.FRIESIAN)
        url = reverse('dairy:cow-breeds-list')
        url += '?ordering=-name'
        headers = {'Authorization': f'Token {self.farm_manager_token}'}
        response = self.client.get(url, headers=headers)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 6
        assert response.data[0]['name'] == CowBreedChoices.SAHIWAL
        assert response.data[1]['name'] == CowBreedChoices.JERSEY
        assert response.data[2]['name'] == CowBreedChoices.GUERNSEY
        assert response.data[3]['name'] == CowBreedChoices.FRIESIAN
        assert response.data[4]['name'] == CowBreedChoices.CROSSBREED
        assert response.data[5]['name'] == CowBreedChoices.AYRSHIRE

    def test_no_results_for_invalid_name(self):
        # Test filtering with a name that doesn't exist
        url = reverse('dairy:cow-breeds-list')
        url += '?name=nonexistent'
        headers = {'Authorization': f'Token {self.farm_worker_token}'}
        response = self.client.get(url, headers=headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data == {'detail': 'No cow breed(s) found matching the provided filters.'}
