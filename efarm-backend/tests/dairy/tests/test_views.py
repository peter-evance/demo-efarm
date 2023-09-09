import pytest
from django.urls import reverse

from dairy.views import *


@pytest.mark.django_db
class TestCowViewSet:
    @pytest.fixture(autouse=True)
    def setup(self, setup_users, setup_cows):
        self.client = setup_users['client']

        self.regular_user_token = setup_users['regular_user_token']
        self.farm_owner_token = setup_users['farm_owner_token']
        self.farm_manager_token = setup_users['farm_manager_token']
        self.asst_farm_manager_token = setup_users['asst_farm_manager_token']
        self.team_leader_token = setup_users['team_leader_token']
        self.farm_worker_token = setup_users['farm_worker_token']

        self.general_cow = setup_cows

    def test_add_cow_as_farm_owner(self):
        """
        Test adding a cow as a farm owner.
        """
        response = self.client.post(reverse('dairy:cows-list'), data=self.general_cow, format='json',
                                    HTTP_AUTHORIZATION=f'Token {self.farm_owner_token}')
        assert response.status_code == status.HTTP_201_CREATED
        assert Cow.objects.filter(name=self.general_cow['name']).exists()

    def test_add_cow_as_farm_manager(self):
        """
        Test adding a cow as a farm manager.
        """
        response = self.client.post(reverse('dairy:cows-list'), data=self.general_cow, format='json',
                                    HTTP_AUTHORIZATION=f'Token {self.farm_manager_token}')
        assert response.status_code == status.HTTP_201_CREATED
        assert Cow.objects.filter(name=self.general_cow['name']).exists()

    def test_add_cow_asst_farm_manager_permission_denied(self):
        """
        Test adding a cow as an assistant farm manager (should be denied).
        """
        response = self.client.post(reverse('dairy:cows-list'), data=self.general_cow, format='json',
                                    HTTP_AUTHORIZATION=f'Token {self.asst_farm_manager_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_add_cow_as_team_leader_permission_denied(self):
        """
        Test adding a cow as a team leader (should be denied).
        """
        response = self.client.post(reverse('dairy:cows-list'), data=self.general_cow, format='json',
                                    HTTP_AUTHORIZATION=f'Token {self.team_leader_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_add_cow_as_farm_worker_permission_denied(self):
        """
        Test adding a cow as a farm worker (should be denied).
        """
        response = self.client.post(reverse('dairy:cows-list'), data=self.general_cow, format='json',
                                    HTTP_AUTHORIZATION=f'Token {self.farm_worker_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_add_cow_as_regular_user_permission_denied(self):
        """
        Test adding a cow as a regular user (should be denied).
        """
        response = self.client.post(reverse('dairy:cows-list'), data=self.general_cow, format='json',
                                    HTTP_AUTHORIZATION=f'Token {self.regular_user_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_add_cow_without_authentication(self):
        """
        Test adding a cow without authentication (should be denied).
        """
        response = self.client.post(reverse('dairy:cows-list'), data=self.general_cow, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_view_cow_as_farm_owner(self):
        """
        Test viewing cows as a farm owner.
        """
        response = self.client.get(reverse('dairy:cows-list'), format='json',
                                   HTTP_AUTHORIZATION=f'Token {self.farm_owner_token}')
        assert response.status_code == status.HTTP_200_OK

    def test_view_cow_as_farm_manager(self):
        """
        Test viewing cows as a farm manager.
        """
        response = self.client.get(reverse('dairy:cows-list'), format='json',
                                   HTTP_AUTHORIZATION=f'Token {self.farm_manager_token}')
        assert response.status_code == status.HTTP_200_OK

    def test_view_cow_as_asst_farm_manager(self):
        """
        Test viewing cows as an assistant farm manager.
        """
        response = self.client.get(reverse('dairy:cows-list'), format='json',
                                   HTTP_AUTHORIZATION=f'Token {self.asst_farm_manager_token}')
        assert response.status_code == status.HTTP_200_OK

    def test_view_cow_as_team_leader(self):
        """
        Test viewing cows as a team leader.
        """
        response = self.client.get(reverse('dairy:cows-list'), format='json',
                                   HTTP_AUTHORIZATION=f'Token {self.team_leader_token}')
        assert response.status_code == status.HTTP_200_OK

    def test_view_cow_as_farm_worker(self):
        """
        Test viewing cows as a farm worker.
        """
        response = self.client.get(reverse('dairy:cows-list'), format='json',
                                   HTTP_AUTHORIZATION=f'Token {self.farm_worker_token}')
        assert response.status_code == status.HTTP_200_OK

    def test_view_cow_as_regular_users_permission_denied(self):
        """
        Test viewing cows as regular users (should be denied).
        """
        response = self.client.get(reverse('dairy:cows-list'), format='json',
                                   HTTP_AUTHORIZATION=f'Token {self.regular_user_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_view_cow_without_authentication(self):
        """
        Test viewing cows without authentication (should be denied).
        """
        response = self.client.get(reverse('dairy:cows-list'), format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_view_cow_detail_as_farm_owner(self):
        """
        Test viewing cow details as a farm owner.
        """
        serializer = CowSerializer(data=self.general_cow)
        assert serializer.is_valid()
        cow = serializer.save()
        response = self.client.get(reverse('dairy:cows-detail', kwargs={'pk': cow.pk}), format='json',
                                   HTTP_AUTHORIZATION=f'Token {self.farm_owner_token}')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == cow.name

    def test_view_cow_detail_as_farm_manager(self):
        """
        Test viewing cow details as a farm manager.
        """
        serializer = CowSerializer(data=self.general_cow)
        assert serializer.is_valid()
        cow = serializer.save()
        response = self.client.get(reverse('dairy:cows-detail', kwargs={'pk': cow.pk}), format='json',
                                   HTTP_AUTHORIZATION=f'Token {self.farm_manager_token}')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == cow.name

    def test_view_cow_detail_as_asst_farm_manager(self):
        """
        Test viewing cow details as an assistant farm manager.
        """
        serializer = CowSerializer(data=self.general_cow)
        assert serializer.is_valid()
        cow = serializer.save()
        response = self.client.get(reverse('dairy:cows-detail', kwargs={'pk': cow.pk}), format='json',
                                   HTTP_AUTHORIZATION=f'Token {self.asst_farm_manager_token}')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == cow.name

    def test_view_cow_detail_as_team_leader(self):
        """
        Test viewing cow details as a team leader.
        """
        serializer = CowSerializer(data=self.general_cow)
        assert serializer.is_valid()
        cow = serializer.save()
        response = self.client.get(reverse('dairy:cows-detail', kwargs={'pk': cow.pk}), format='json',
                                   HTTP_AUTHORIZATION=f'Token {self.team_leader_token}')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == cow.name

    def test_view_cow_detail_as_farm_worker(self):
        """
        Test viewing cow details as a farm worker.
        """
        serializer = CowSerializer(data=self.general_cow)
        assert serializer.is_valid()
        cow = serializer.save()
        response = self.client.get(reverse('dairy:cows-detail', kwargs={'pk': cow.pk}), format='json',
                                   HTTP_AUTHORIZATION=f'Token {self.farm_worker_token}')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == cow.name

    def test_view_cow_detail_as_regular_user_permission_denied(self):
        """
        Test viewing cow details as a regular user (should be denied).
        """
        serializer = CowSerializer(data=self.general_cow)
        assert serializer.is_valid()
        cow = serializer.save()
        response = self.client.get(reverse('dairy:cows-detail', kwargs={'pk': cow.pk}), format='json',
                                   HTTP_AUTHORIZATION=f'Token {self.regular_user_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_view_cow_detail_without_authentication(self):
        """
        Test viewing cow details without authentication (should be denied).
        """
        serializer = CowSerializer(data=self.general_cow)
        assert serializer.is_valid()
        cow = serializer.save()
        response = self.client.get(reverse('dairy:cows-detail', kwargs={'pk': cow.pk}), format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_cow_detail_as_farm_owner(self):
        """
        Test updating cow details as a farm owner.
        """
        serializer = CowSerializer(data=self.general_cow)
        assert serializer.is_valid()
        cow = serializer.save()
        data = {'name': 'Updated Cow'}

        response = self.client.patch(reverse('dairy:cows-detail', kwargs={'pk': cow.pk}), data=data, format='json',
                                     HTTP_AUTHORIZATION=f'Token {self.farm_owner_token}')
        assert response.status_code == status.HTTP_200_OK
        assert Cow.objects.get(pk=cow.pk).name == 'Updated Cow'

    def test_update_cow_detail_as_farm_manager(self):
        """
        Test updating cow details as a farm manager.
        """
        serializer = CowSerializer(data=self.general_cow)
        assert serializer.is_valid()
        cow = serializer.save()
        data = {'name': 'Updated Cow'}

        response = self.client.patch(reverse('dairy:cows-detail', kwargs={'pk': cow.pk}), data=data, format='json',
                                     HTTP_AUTHORIZATION=f'Token {self.farm_manager_token}')
        assert response.status_code == status.HTTP_200_OK
        assert Cow.objects.get(pk=cow.pk).name == 'Updated Cow'

    def test_update_cow_detail_as_asst_farm_manager_permission_denied(self):
        """
        Test updating cow details as an assistant farm manager (should be denied).
        """
        serializer = CowSerializer(data=self.general_cow)
        assert serializer.is_valid()
        cow = serializer.save()
        data = {'name': 'Updated Cow'}

        response = self.client.patch(reverse('dairy:cows-detail', kwargs={'pk': cow.pk}), data=data, format='json',
                                     HTTP_AUTHORIZATION=f'Token {self.asst_farm_manager_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Cow.objects.get(pk=cow.pk).name != 'Updated Cow'

    def test_update_cow_detail_as_team_leader_permission_denied(self):
        """
        Test updating cow details as a team leader (should be denied).
        """
        serializer = CowSerializer(data=self.general_cow)
        assert serializer.is_valid()
        cow = serializer.save()
        data = {'name': 'Updated Cow'}
        response = self.client.patch(reverse('dairy:cows-detail', kwargs={'pk': cow.pk}), data=data, format='json',
                                     HTTP_AUTHORIZATION=f'Token {self.team_leader_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Cow.objects.get(pk=cow.pk).name != 'Updated Cow'

    def test_update_cow_detail_as_farm_worker_permission_denied(self):
        """
        Test updating cow details as a farm worker (should be denied).
        """
        serializer = CowSerializer(data=self.general_cow)
        assert serializer.is_valid()
        cow = serializer.save()
        data = {'name': 'Updated Cow'}

        response = self.client.patch(reverse('dairy:cows-detail', kwargs={'pk': cow.pk}), data=data, format='json',
                                     HTTP_AUTHORIZATION=f'Token {self.farm_worker_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Cow.objects.get(pk=cow.pk).name != 'Updated Cow'

    def test_update_cow_detail_as_regular_user_permission_denied(self):
        """
        Test updating cow details as a regular user (should be denied).
        """
        serializer = CowSerializer(data=self.general_cow)
        assert serializer.is_valid()
        cow = serializer.save()
        data = {'name': 'Updated Cow'}
        response = self.client.patch(reverse('dairy:cows-detail', kwargs={'pk': cow.pk}), data=data, format='json',
                                     HTTP_AUTHORIZATION=f'Token {self.regular_user_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Cow.objects.get(pk=cow.pk).name != 'Updated Cow'

    def test_update_cow_detail_without_authentication(self):
        """
        Test updating cow details without authentication (should be denied).
        """
        serializer = CowSerializer(data=self.general_cow)
        assert serializer.is_valid()
        cow = serializer.save()
        data = {'name': 'Updated Cow'}
        response = self.client.patch(reverse('dairy:cows-detail', kwargs={'pk': cow.pk}), data=data, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert Cow.objects.get(pk=cow.pk).name != 'Updated Cow'

    def test_delete_cow_as_farm_owner(self):
        """
        Test deleting cow details as a farm owner.
        """
        serializer = CowSerializer(data=self.general_cow)
        assert serializer.is_valid()
        cow = serializer.save()

        response = self.client.delete(reverse('dairy:cows-detail', kwargs={'pk': cow.pk}), format='json',
                                      HTTP_AUTHORIZATION=f'Token {self.farm_owner_token}')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Cow.objects.filter(pk=cow.pk).exists()

    def test_delete_cow_as_farm_manager_permission_denied(self):
        """
        Test deleting cow details as a farm manager (should be denied).
        """
        serializer = CowSerializer(data=self.general_cow)
        assert serializer.is_valid()
        cow = serializer.save()
        response = self.client.delete(reverse('dairy:cows-detail', kwargs={'pk': cow.pk}), format='json',
                                      HTTP_AUTHORIZATION=f'Token {self.farm_manager_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Cow.objects.filter(pk=cow.pk).exists()

    def test_delete_cow_as_asst_farm_manager_permission_denied(self):
        """
        Test deleting cow details as an assistant farm manager (should be denied).
        """
        serializer = CowSerializer(data=self.general_cow)
        assert serializer.is_valid()
        cow = serializer.save()
        response = self.client.delete(reverse('dairy:cows-detail', kwargs={'pk': cow.pk}), format='json',
                                      HTTP_AUTHORIZATION=f'Token {self.asst_farm_manager_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Cow.objects.filter(pk=cow.pk).exists()

    def test_delete_cow_as_team_leader_permission_denied(self):
        """
        Test deleting cow details as a team leader (should be denied).
        """
        serializer = CowSerializer(data=self.general_cow)
        assert serializer.is_valid()
        cow = serializer.save()
        response = self.client.delete(reverse('dairy:cows-detail', kwargs={'pk': cow.pk}), format='json',
                                      HTTP_AUTHORIZATION=f'Token {self.team_leader_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Cow.objects.filter(pk=cow.pk).exists()

    def test_delete_cow_as_farm_worker_permission_denied(self):
        """
        Test deleting cow details as a farm worker (should be denied).
        """
        serializer = CowSerializer(data=self.general_cow)
        assert serializer.is_valid()
        cow = serializer.save()
        response = self.client.delete(reverse('dairy:cows-detail', kwargs={'pk': cow.pk}), format='json',
                                      HTTP_AUTHORIZATION=f'Token {self.farm_worker_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Cow.objects.filter(pk=cow.pk).exists()

    def test_filter_cows_by_name(self):
        serializer = CowSerializer(data=self.general_cow)
        assert serializer.is_valid()
        cow = serializer.save()
        url = reverse('dairy:cows-list')
        url += f"?name={'General'}"
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Token {self.farm_owner_token}')
        assert response.status_code == status.HTTP_200_OK

    def test_filter_cows_by_breed_name(self):
        serializer = CowSerializer(data=self.general_cow)
        assert serializer.is_valid()
        cow = serializer.save()
        url = reverse('dairy:cows-list')
        url += f"?breed={'Ayrshire'}"
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Token {self.farm_owner_token}')
        assert response.status_code == status.HTTP_200_OK

    def test_filter_cows_by_category(self):
        serializer = CowSerializer(data=self.general_cow)
        assert serializer.is_valid()
        cow = serializer.save()
        url = reverse('dairy:cows-list')
        url += f"?category={'Heifer'}"
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Token {self.farm_owner_token}')
        assert response.status_code == status.HTTP_200_OK

    def test_filter_cows_by_gender(self):
        serializer = CowSerializer(data=self.general_cow)
        assert serializer.is_valid()
        cow = serializer.save()
        url = reverse('dairy:cows-list')
        url += f"?gender={'Female'}"
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Token {self.farm_owner_token}')
        assert response.status_code == status.HTTP_200_OK

    def test_filter_cows_by_availability_status(self):
        serializer = CowSerializer(data=self.general_cow)
        assert serializer.is_valid()
        cow = serializer.save()
        url = reverse('dairy:cows-list')
        url += f"?availability_status={'Alive'}"
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Token {self.farm_owner_token}')
        assert response.status_code == status.HTTP_200_OK

    def test_filter_cows_by_year_of_birth(self):
        serializer = CowSerializer(data=self.general_cow)
        assert serializer.is_valid()
        cow = serializer.save()
        url = reverse('dairy:cows-list')
        url += f"?year_of_birth={'2022'}"
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Token {self.farm_owner_token}')
        assert response.status_code == status.HTTP_200_OK

    def test_ordering_cows_by_date_of_birth(self):
        serializer = CowSerializer(data=self.general_cow)
        assert serializer.is_valid()
        cow = serializer.save()
        url = reverse('dairy:cows-list')
        url += f"?ordering={'date_of_birth'}"
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Token {self.farm_owner_token}')
        assert response.status_code == status.HTTP_200_OK

    def test_ordering_cows_by_gender(self):
        serializer = CowSerializer(data=self.general_cow)
        assert serializer.is_valid()
        cow = serializer.save()
        url = reverse('dairy:cows-list')
        url += f"?ordering={'gender'}"
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Token {self.farm_owner_token}')
        assert response.status_code == status.HTTP_200_OK

    def test_ordering_cows_by_breed(self):
        serializer = CowSerializer(data=self.general_cow)
        assert serializer.is_valid()
        cow = serializer.save()
        url = reverse('dairy:cows-list')
        url += f"?ordering={'breed'}"
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Token {self.farm_owner_token}')
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestCowBreedViewSet:
    @pytest.fixture(autouse=True)
    def setup(self, setup_users):
        self.client = setup_users['client']

        self.regular_user_token = setup_users['regular_user_token']
        self.farm_owner_token = setup_users['farm_owner_token']
        self.farm_manager_token = setup_users['farm_manager_token']
        self.asst_farm_manager_token = setup_users['asst_farm_manager_token']
        self.team_leader_token = setup_users['team_leader_token']
        self.farm_worker_token = setup_users['farm_worker_token']

    def test_create_cow_breed_as_farm_owner(self):
        """
        Test creating a cow breed by a farm owner.
        """
        cow_breed_data = {'name': CowBreedChoices.GUERNSEY}
        response = self.client.post(reverse('dairy:cow-breeds-list'), data=cow_breed_data,
                                    HTTP_AUTHORIZATION=f'Token {self.farm_owner_token}')
        assert response.status_code == status.HTTP_201_CREATED
        assert CowBreed.objects.filter(name=cow_breed_data['name']).exists()

    def test_create_cow_breed_as_farm_manager(self):
        """
        Test creating a cow breed by a farm manager
        """
        cow_breed_data = {'name': CowBreedChoices.GUERNSEY}
        response = self.client.post(
            reverse('dairy:cow-breeds-list'), cow_breed_data, HTTP_AUTHORIZATION=f'Token {self.farm_manager_token}')
        assert response.status_code == status.HTTP_201_CREATED
        assert CowBreed.objects.filter(name=cow_breed_data['name']).exists()

    def test_create_cow_breed_as_asst_farm_manager_permission_denied(self):
        """
        Test creating a cow breed by a assistant farm manager (should be denied).
        """
        cow_breed_data = {'name': CowBreedChoices.GUERNSEY}
        response = self.client.post(
            reverse('dairy:cow-breeds-list'), cow_breed_data,
            HTTP_AUTHORIZATION=f'Token {self.asst_farm_manager_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not CowBreed.objects.filter(name=cow_breed_data['name']).exists()

    def test_create_cow_breed_as_team_leader_permission_denied(self):
        """
        Test creating a cow breed by a team leader (should be denied).
        """
        cow_breed_data = {'name': CowBreedChoices.GUERNSEY}
        response = self.client.post(
            reverse('dairy:cow-breeds-list'), cow_breed_data, HTTP_AUTHORIZATION=f'Token {self.team_leader_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not CowBreed.objects.filter(name=cow_breed_data['name']).exists()

    def test_create_cow_breed_as_farm_worker_permission_denied(self):
        """
        Test creating a cow breed by a farm worker (should be denied).
        """
        cow_breed_data = {'name': CowBreedChoices.AYRSHIRE}
        response = self.client.post(reverse('dairy:cow-breeds-list'), cow_breed_data,
                                    HTTP_AUTHORIZATION=f'Token {self.farm_worker_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not CowBreed.objects.filter(name=cow_breed_data['name']).exists()

    def test_create_cow_breed_as_regular_user_permission_denied(self):
        """
        Test creating a cow breed by a regular user (should be denied).
        """
        cow_breed_data = {'name': CowBreedChoices.AYRSHIRE}
        response = self.client.post(reverse('dairy:cow-breeds-list'), cow_breed_data,
                                    HTTP_AUTHORIZATION=f'Token {self.regular_user_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not CowBreed.objects.filter(name=cow_breed_data['name']).exists()

    def test_create_cow_breed_without_authentication(self):
        """
        Test creating a cow breed without authentication (should be denied).
        """
        cow_breed_data = {'name': CowBreedChoices.AYRSHIRE}
        response = self.client.post(reverse('dairy:cow-breeds-list'), cow_breed_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert not CowBreed.objects.filter(name=cow_breed_data['name']).exists()

    def test_retrieve_cow_breeds_as_farm_owner(self):
        """
        Test retrieving cow breeds by a farm owner.
        """
        response = self.client.get(reverse('dairy:cow-breeds-list'),
                                   HTTP_AUTHORIZATION=f'Token {self.farm_owner_token}')
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_cow_breeds_as_farm_manager(self):
        """
        Test retrieving cow breeds by a farm manager.
        """
        response = self.client.get(reverse('dairy:cow-breeds-list'),
                                   HTTP_AUTHORIZATION=f'Token {self.farm_manager_token}')
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_cow_breeds_as_asst_farm_manager(self):
        """
        Test retrieving cow breeds by an assistant farm manager.
        """
        response = self.client.get(reverse('dairy:cow-breeds-list'),
                                   HTTP_AUTHORIZATION=f'Token {self.asst_farm_manager_token}')
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_cow_breeds_as_team_leader(self):
        """
        Test retrieving cow breeds by a team leader.
        """
        response = self.client.get(reverse('dairy:cow-breeds-list'),
                                   HTTP_AUTHORIZATION=f'Token {self.team_leader_token}')
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_cow_breeds_as_regular_user_permission_denied(self):
        """
        Test retrieving cow breeds by a regular user (should be denied).
        """
        response = self.client.get(reverse('dairy:cow-breeds-list'),
                                   HTTP_AUTHORIZATION=f'Token {self.regular_user_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_retrieve_cow_breeds_without_authentication(self):
        """
        Test retrieving cow breeds without authentication (should be denied).
        """
        url = reverse('dairy:cow-breeds-list')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_cow_breed_permission_denied(self):
        """
        Test updating a cow breed (should be denied).
        """
        cow_breed = CowBreed.objects.create(name=CowBreedChoices.FRIESIAN)
        url = reverse('dairy:cow-breeds-detail', kwargs={'pk': cow_breed.id})
        cow_breed_update_data = {'name': CowBreedChoices.AYRSHIRE}
        response = self.client.put(url, cow_breed_update_data, HTTP_AUTHORIZATION=f'Token {self.farm_owner_token}')
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    def test_delete_cow_breed_as_farm_owner(self):
        """
        Test deleting a cow breed by a farm owner.
        """
        cow_breed = CowBreed.objects.create(name=CowBreedChoices.FRIESIAN)
        url = reverse('dairy:cow-breeds-detail', kwargs={'pk': cow_breed.id})
        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Token {self.farm_owner_token}')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not CowBreed.objects.filter(id=cow_breed.id).exists()

    def test_delete_cow_breed_as_farm_manager(self):
        """
        Test deleting a cow breed by a farm manager.
        """
        cow_breed = CowBreed.objects.create(name=CowBreedChoices.SAHIWAL)
        url = reverse('dairy:cow-breeds-detail', kwargs={'pk': cow_breed.id})
        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Token {self.farm_manager_token}')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not CowBreed.objects.filter(id=cow_breed.id).exists()

    def test_delete_cow_breed_as_asst_farm_manager_permission_denied(self):
        """
        Test deleting a cow breed by an assistant farm manager (should be denied).
        """
        cow_breed = CowBreed.objects.create(name=CowBreedChoices.CROSSBREED)
        url = reverse('dairy:cow-breeds-detail', kwargs={'pk': cow_breed.id})
        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Token {self.asst_farm_manager_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert CowBreed.objects.filter(id=cow_breed.id).exists()

    def test_delete_cow_breed_as_team_leader_permission_denied(self):
        """
        Test deleting a cow breed by a team leader (should be denied).
        """
        cow_breed = CowBreed.objects.create(name=CowBreedChoices.CROSSBREED)
        url = reverse('dairy:cow-breeds-detail', kwargs={'pk': cow_breed.id})
        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Token {self.team_leader_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert CowBreed.objects.filter(id=cow_breed.id).exists()

    def test_delete_cow_breed_as_farm_worker_permission_denied(self):
        """
        Test deleting a cow breed by a farm worker (should be denied).
        """
        cow_breed = CowBreed.objects.create(name=CowBreedChoices.CROSSBREED)
        url = reverse('dairy:cow-breeds-detail', kwargs={'pk': cow_breed.id})
        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Token {self.farm_worker_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert CowBreed.objects.filter(id=cow_breed.id).exists()

    def test_delete_cow_breed_as_regular_user_permission_denied(self):
        '''
        Test delete cow breed as a regular user (permission denied)
        '''
        cow_breed = CowBreed.objects.create(name=CowBreedChoices.SAHIWAL)
        url = reverse('dairy:cow-breeds-detail', kwargs={'pk': cow_breed.id})

        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Token {self.regular_user_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert CowBreed.objects.filter(id=cow_breed.id).exists()

    def test_delete_cow_breed_unauthorized(self):
        '''
        Test delete cow breed by unauthorized request
        '''
        cow_breed = CowBreed.objects.create(name=CowBreedChoices.SAHIWAL)
        url = reverse('dairy:cow-breeds-detail', kwargs={'pk': cow_breed.id})

        response = self.client.delete(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert CowBreed.objects.filter(id=cow_breed.id).exists()

    def test_filter_cow_breeds_by_name(self):
        """
        Test filtering cow breeds by name (e.g., get all breeds with name 'Jersey').
        """
        CowBreed.objects.create(name=CowBreedChoices.JERSEY)
        CowBreed.objects.create(name=CowBreedChoices.CROSSBREED)
        url = reverse('dairy:cow-breeds-list')
        url += f'?name={CowBreedChoices.JERSEY}'

        response = self.client.get(url, HTTP_AUTHORIZATION=f'Token {self.farm_owner_token}')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['name'] == CowBreedChoices.JERSEY

    def test_filter_cow_breeds_by_partial_name(self):
        """
        Test filtering cow breeds by partial name (e.g., get breeds with names containing 'ey').
        """
        CowBreed.objects.create(name=CowBreedChoices.JERSEY)
        CowBreed.objects.create(name=CowBreedChoices.GUERNSEY)
        url = reverse('dairy:cow-breeds-list')
        url += '?name=ey'

        response = self.client.get(url, HTTP_AUTHORIZATION=f'Token {self.asst_farm_manager_token}')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        assert [cow_breed['name'] for cow_breed in response.data] == [CowBreedChoices.JERSEY,
                                                                      CowBreedChoices.GUERNSEY]

    def test_order_cow_breeds_by_multiple_fields(self):
        """
        Test ordering cow breeds by multiple fields (e.g., name in descending order, id in ascending order).
        """
        CowBreed.objects.create(name=CowBreedChoices.JERSEY)
        CowBreed.objects.create(name=CowBreedChoices.GUERNSEY)
        CowBreed.objects.create(name=CowBreedChoices.CROSSBREED)
        CowBreed.objects.create(name=CowBreedChoices.SAHIWAL)
        CowBreed.objects.create(name=CowBreedChoices.AYRSHIRE)
        CowBreed.objects.create(name=CowBreedChoices.FRIESIAN)
        url = reverse('dairy:cow-breeds-list')
        url += '?ordering=-name'

        response = self.client.get(url, HTTP_AUTHORIZATION=f'Token {self.farm_manager_token}')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 6
        assert response.data[0]['name'] == CowBreedChoices.SAHIWAL
        assert response.data[1]['name'] == CowBreedChoices.JERSEY
        assert response.data[2]['name'] == CowBreedChoices.GUERNSEY
        assert response.data[3]['name'] == CowBreedChoices.FRIESIAN
        assert response.data[4]['name'] == CowBreedChoices.CROSSBREED
        assert response.data[5]['name'] == CowBreedChoices.AYRSHIRE

    def test_no_results_for_invalid_name(self):
        """
        Test filtering with a name that doesn't exist.
        """
        url = reverse('dairy:cow-breeds-list')
        url += '?name=nonexistent'
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Token {self.farm_worker_token}')
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data == {'detail': 'No cow breed(s) found matching the provided filters.'}


@pytest.mark.django_db
class TestHeatViewSet:
    @pytest.fixture(autouse=True)
    def setup(self, setup_users, setup_cows):
        self.client = setup_users["client"]

        self.regular_user_token = setup_users["regular_user_token"]
        self.farm_owner_token = setup_users["farm_owner_token"]
        self.farm_manager_token = setup_users["farm_manager_token"]
        self.asst_farm_manager_token = setup_users["asst_farm_manager_token"]
        self.team_leader_token = setup_users["team_leader_token"]
        self.farm_worker_token = setup_users["farm_worker_token"]

        self.general_cow = setup_cows

    def test_add_heat_record_as_farm_owner(self):
        """
        Test adding a heat record as a farm owner.
        """
        serializer = CowSerializer(data=self.general_cow)
        assert serializer.is_valid()
        cow = serializer.save()

        heat_data = {
            "observation_time": timezone.now(),
            "cow": cow.id,
        }

        response = self.client.post(
            reverse("dairy:heat-records-list"),
            data=heat_data,
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.farm_owner_token}",
        )
        assert response.status_code == 201

    def test_add_heat_record_as_farm_manager(self):
        """
        Test adding a heat record as a farm manager.
        """
        serializer = CowSerializer(data=self.general_cow)
        assert serializer.is_valid()
        cow = serializer.save()

        heat_data = {
            "observation_time": timezone.now(),
            "cow": cow.id,
        }

        response = self.client.post(
            reverse("dairy:heat-records-list"),
            data=heat_data,
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.farm_manager_token}",
        )
        assert response.status_code == 201
        assert Heat.objects.filter(cow=cow).exists()

    def test_add_heat_record_as_asst_farm_manager(self):
        """
        Test adding a heat record as an assistant farm manager.
        """
        serializer = CowSerializer(data=self.general_cow)
        assert serializer.is_valid()
        cow = serializer.save()

        heat_data = {
            "observation_time": timezone.now(),
            "cow": cow.id,
        }

        response = self.client.post(
            reverse("dairy:heat-records-list"),
            data=heat_data,
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.asst_farm_manager_token}",
        )
        assert response.status_code == 201
        assert Heat.objects.filter(cow=cow).exists()

    def test_add_heat_record_as_team_leader(self):
        """
        Test adding a heat record as a team leader.
        """
        serializer = CowSerializer(data=self.general_cow)
        assert serializer.is_valid()
        cow = serializer.save()

        heat_data = {
            "observation_time": timezone.now(),
            "cow": cow.id,
        }

        response = self.client.post(
            reverse("dairy:heat-records-list"),
            data=heat_data,
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.team_leader_token}",
        )
        assert response.status_code == 201
        assert Heat.objects.filter(cow=cow).exists()

    def test_add_heat_record_as_farm_worker(self):
        """
        Test adding a heat record as a farm worker.
        """
        serializer = CowSerializer(data=self.general_cow)
        assert serializer.is_valid()
        cow = serializer.save()

        heat_data = {
            "observation_time": timezone.now(),
            "cow": cow.id,
        }

        response = self.client.post(
            reverse("dairy:heat-records-list"),
            data=heat_data,
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.farm_worker_token}",
        )
        assert response.status_code == 201
        assert Heat.objects.filter(cow=cow).exists()

    def test_add_heat_record_without_authentication(self):
        """
        Test adding a heat record without authentication.
        """
        serializer = CowSerializer(data=self.general_cow)
        assert serializer.is_valid()
        cow = serializer.save()

        heat_data = {
            "observation_time": timezone.now(),
            "cow": cow.id,
        }

        response = self.client.post(
            reverse("dairy:heat-records-list"), data=heat_data, format="json"
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert not Heat.objects.filter(cow=cow).exists()

    def test_view_heat_records_as_farm_owner(self):
        """
        Test viewing heat records as a farm owner.
        """
        response = self.client.get(
            reverse("dairy:heat-records-list"),
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.farm_owner_token}",
        )
        assert response.status_code == status.HTTP_200_OK

    def test_view_heat_records_as_farm_manager(self):
        """
        Test viewing heat records as a farm manager.
        """
        response = self.client.get(
            reverse("dairy:heat-records-list"),
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.farm_manager_token}",
        )
        assert response.status_code == status.HTTP_200_OK

    def test_view_heat_records_as_asst_farm_manager(self):
        """
        Test viewing heat records as an assistant farm manager.
        """
        response = self.client.get(
            reverse("dairy:heat-records-list"),
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.asst_farm_manager_token}",
        )
        assert response.status_code == status.HTTP_200_OK

    def test_view_heat_records_as_team_leader(self):
        """
        Test viewing heat records as a team leader.
        """
        response = self.client.get(
            reverse("dairy:heat-records-list"),
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.team_leader_token}",
        )
        assert response.status_code == status.HTTP_200_OK

    def test_view_heat_records_as_farm_worker(self):
        """
        Test viewing heat records as a farm worker.
        """
        response = self.client.get(
            reverse("dairy:heat-records-list"),
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.farm_worker_token}",
        )
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestInseminatorViewSet:
    @pytest.fixture(autouse=True)
    def setup(self, setup_users, setup_inseminators_data):
        self.client = setup_users["client"]

        self.regular_user_token = setup_users["regular_user_token"]
        self.farm_owner_token = setup_users["farm_owner_token"]
        self.farm_manager_token = setup_users["farm_manager_token"]
        self.asst_farm_manager_token = setup_users["asst_farm_manager_token"]
        self.team_leader_token = setup_users["team_leader_token"]
        self.farm_worker_token = setup_users["farm_worker_token"]

        self.inseminators_data = setup_inseminators_data

    def test_add_inseminator_as_farm_owner(self):
        """
        Test adding an inseminator as a farm owner.
        """
        response = self.client.post(
            reverse("dairy:inseminator-records-list"),
            data=self.inseminators_data,
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.farm_owner_token}",
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert Inseminator.objects.filter(
            license_number=self.inseminators_data["license_number"]
        ).exists()

    def test_add_inseminator_as_farm_manager(self):
        """
        Test adding an inseminator as a farm manager.
        """
        response = self.client.post(
            reverse("dairy:inseminator-records-list"),
            data=self.inseminators_data,
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.farm_manager_token}",
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert Inseminator.objects.filter(
            license_number=self.inseminators_data["license_number"]
        ).exists()

    def test_add_inseminator_as_asst_farm_manager(self):
        """
        Test adding an inseminator as an assistant farm manager.
        """
        response = self.client.post(
            reverse("dairy:inseminator-records-list"),
            data=self.inseminators_data,
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.asst_farm_manager_token}",
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert Inseminator.objects.filter(
            license_number=self.inseminators_data["license_number"]
        ).exists()

    def test_add_inseminator_as_team_leader_permission_denied(self):
        """
        Test adding an inseminator as a team leader (permission denied).
        """
        response = self.client.post(
            reverse("dairy:inseminator-records-list"),
            data=self.inseminators_data,
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.team_leader_token}",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not Inseminator.objects.filter(
            license_number=self.inseminators_data["license_number"]
        ).exists()

    def test_add_inseminator_as_farm_worker_permission_denied(self):
        """
        Test adding an inseminator as a farm worker (permission denied).
        """
        response = self.client.post(
            reverse("dairy:inseminator-records-list"),
            data=self.inseminators_data,
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.farm_worker_token}",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not Inseminator.objects.filter(
            license_number=self.inseminators_data["license_number"]
        ).exists()

    def test_add_inseminator_as_regular_user_permission_denied(self):
        """
        Test adding an inseminator as a regular user (permission denied).
        """
        response = self.client.post(
            reverse("dairy:inseminator-records-list"),
            data=self.inseminators_data,
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.regular_user_token}",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not Inseminator.objects.filter(
            license_number=self.inseminators_data["license_number"]
        ).exists()

    def test_add_inseminator_without_authentication(self):
        """
        Test adding an inseminator without authentication.
        """
        response = self.client.post(
            reverse("dairy:inseminator-records-list"),
            data=self.inseminators_data,
            format="json",
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert not Inseminator.objects.filter(
            license_number=self.inseminators_data["license_number"]
        ).exists()

    def test_update_inseminator_as_farm_owner(self):
        """
        Test updating an inseminator as a farm owner.
        """
        serializer = InseminatorSerializer(data=self.inseminators_data)
        assert serializer.is_valid()
        inseminator = serializer.save()
        updated_license_number = {"license_number": "UPDATED123"}

        response = self.client.patch(
            reverse("dairy:inseminator-records-detail", kwargs={"pk": inseminator.pk}),
            data=updated_license_number,
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.farm_owner_token}",
        )
        assert response.status_code == status.HTTP_200_OK
        assert Inseminator.objects.filter(
            license_number=updated_license_number["license_number"]
        ).exists()

    def test_update_inseminator_as_farm_manager(self):
        """
        Test updating an inseminator as a farm manager.
        """
        serializer = InseminatorSerializer(data=self.inseminators_data)
        assert serializer.is_valid()
        inseminator = serializer.save()

        updated_license_number = {"license_number": "UPDATED123"}

        response = self.client.patch(
            reverse("dairy:inseminator-records-detail", kwargs={"pk": inseminator.pk}),
            data=updated_license_number,
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.farm_manager_token}",
        )
        assert response.status_code == status.HTTP_200_OK
        assert Inseminator.objects.filter(
            license_number=updated_license_number["license_number"]
        ).exists()

    def test_update_inseminator_as_asst_farm_manager(self):
        """
        Test updating an inseminator as an assistant farm manager.
        """
        serializer = InseminatorSerializer(data=self.inseminators_data)
        assert serializer.is_valid()
        inseminator = serializer.save()
        updated_license_number = {"license_number": "UPDATED123"}

        response = self.client.patch(
            reverse("dairy:inseminator-records-detail", kwargs={"pk": inseminator.pk}),
            data=updated_license_number,
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.asst_farm_manager_token}",
        )
        assert response.status_code == status.HTTP_200_OK
        assert Inseminator.objects.filter(
            license_number=updated_license_number["license_number"]
        ).exists()

    def test_update_inseminator_as_team_leader_permission_denied(self):
        """
        Test updating an inseminator as a team leader (permission denied).
        """
        serializer = InseminatorSerializer(data=self.inseminators_data)
        assert serializer.is_valid()
        inseminator = serializer.save()
        updated_license_number = {"license_number": "UPDATED123"}

        response = self.client.patch(
            reverse("dairy:inseminator-records-detail", kwargs={"pk": inseminator.pk}),
            data=updated_license_number,
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.team_leader_token}",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not Inseminator.objects.filter(
            license_number=updated_license_number["license_number"]
        ).exists()

    def test_update_inseminator_as_farm_worker_permission_denied(self):
        """
        Test updating an inseminator as a farm worker (permission denied).
        """
        serializer = InseminatorSerializer(data=self.inseminators_data)
        assert serializer.is_valid()
        inseminator = serializer.save()
        updated_license_number = {"license_number": "UPDATED123"}

        response = self.client.patch(
            reverse("dairy:inseminator-records-detail", kwargs={"pk": inseminator.pk}),
            data=updated_license_number,
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.farm_worker_token}",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not Inseminator.objects.filter(
            license_number=updated_license_number["license_number"]
        ).exists()

    def test_update_inseminator_as_regular_user_permission_denied(self):
        """
        Test updating an inseminator as a regular user (permission denied).
        """
        serializer = InseminatorSerializer(data=self.inseminators_data)
        assert serializer.is_valid()
        inseminator = serializer.save()
        updated_license_number = {"license_number": "UPDATED123"}

        response = self.client.patch(
            reverse("dairy:inseminator-records-detail", kwargs={"pk": inseminator.pk}),
            data=updated_license_number,
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.regular_user_token}",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not Inseminator.objects.filter(
            license_number=updated_license_number["license_number"]
        ).exists()

    def test_update_inseminator_without_authentication(self):
        """
        Test updating an inseminator without authentication.
        """
        serializer = InseminatorSerializer(data=self.inseminators_data)
        assert serializer.is_valid()
        inseminator = serializer.save()
        updated_license_number = {"license_number": "UPDATED123"}

        response = self.client.patch(
            reverse("dairy:inseminator-records-detail", kwargs={"pk": inseminator.pk}),
            data=updated_license_number,
            format="json",
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert not Inseminator.objects.filter(
            license_number=updated_license_number["license_number"]
        ).exists()

    def test_view_inseminator_as_farm_owner(self):
        """
        Test viewing inseminators as a farm owner.
        """
        response = self.client.get(
            reverse("dairy:inseminator-records-list"),
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.farm_owner_token}",
        )
        assert response.status_code == status.HTTP_200_OK

    def test_view_inseminator_as_farm_manager(self):
        """
        Test viewing inseminators as a farm manager.
        """
        response = self.client.get(
            reverse("dairy:inseminator-records-list"),
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.farm_manager_token}",
        )
        assert response.status_code == status.HTTP_200_OK

    def test_view_inseminator_as_asst_farm_manager(self):
        """
        Test viewing inseminators as an assistant farm manager.
        """
        response = self.client.get(
            reverse("dairy:inseminator-records-list"),
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.asst_farm_manager_token}",
        )
        assert response.status_code == status.HTTP_200_OK

    def test_view_inseminator_as_team_leader_permission_denied(self):
        """
        Test viewing inseminators as a team leader (permission denied).
        """
        response = self.client.get(
            reverse("dairy:inseminator-records-list"),
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.team_leader_token}",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_view_inseminator_as_farm_worker_permission_denied(self):
        """
        Test viewing inseminators as a farm worker (permission denied).
        """
        response = self.client.get(
            reverse("dairy:inseminator-records-list"),
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.farm_worker_token}",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_view_inseminator_as_regular_user_permission_denied(self):
        """
        Test viewing inseminators as a regular user (permission denied).
        """
        response = self.client.get(
            reverse("dairy:inseminator-records-list"),
            format="json",
            HTTP_AUTHORIZATION=f"Token {self.regular_user_token}",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_view_inseminator_without_authentication(self):
        """
        Test viewing inseminators without authentication.
        """
        response = self.client.get(
            reverse("dairy:inseminator-records-list"), format="json"
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_inseminator_as_farm_owner(self):
        """
        Test deleting an inseminator as a farm owner.
        """
        serializer = InseminatorSerializer(data=self.inseminators_data)
        assert serializer.is_valid()
        inseminator = serializer.save()

        response = self.client.delete(
            reverse("dairy:inseminator-records-detail", kwargs={"pk": inseminator.pk}),
            HTTP_AUTHORIZATION=f"Token {self.farm_owner_token}",
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Inseminator.objects.filter(pk=inseminator.pk).exists()

    def test_delete_inseminator_as_farm_manager(self):
        """
        Test deleting an inseminator as a farm manager.
        """
        serializer = InseminatorSerializer(data=self.inseminators_data)
        assert serializer.is_valid()
        inseminator = serializer.save()

        response = self.client.delete(
            reverse("dairy:inseminator-records-detail", kwargs={"pk": inseminator.pk}),
            HTTP_AUTHORIZATION=f"Token {self.farm_manager_token}",
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Inseminator.objects.filter(pk=inseminator.pk).exists()

    def test_delete_inseminator_as_asst_farm_manager(self):
        """
        Test deleting an inseminator as an assistant farm manager.
        """
        serializer = InseminatorSerializer(data=self.inseminators_data)
        assert serializer.is_valid()
        inseminator = serializer.save()

        response = self.client.delete(
            reverse("dairy:inseminator-records-detail", kwargs={"pk": inseminator.pk}),
            HTTP_AUTHORIZATION=f"Token {self.asst_farm_manager_token}",
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Inseminator.objects.filter(pk=inseminator.pk).exists()

    def test_delete_inseminator_as_team_leader_permission_denied(self):
        """
        Test deleting an inseminator as a team leader (permission denied).
        """
        serializer = InseminatorSerializer(data=self.inseminators_data)
        assert serializer.is_valid()
        inseminator = serializer.save()

        response = self.client.delete(
            reverse("dairy:inseminator-records-detail", kwargs={"pk": inseminator.pk}),
            HTTP_AUTHORIZATION=f"Token {self.team_leader_token}",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Inseminator.objects.filter(pk=inseminator.pk).exists()

    def test_delete_inseminator_as_farm_worker_permission_denied(self):
        """
        Test deleting an inseminator as a farm worker (permission denied).
        """
        serializer = InseminatorSerializer(data=self.inseminators_data)
        assert serializer.is_valid()
        inseminator = serializer.save()

        response = self.client.delete(
            reverse("dairy:inseminator-records-detail", kwargs={"pk": inseminator.pk}),
            HTTP_AUTHORIZATION=f"Token {self.farm_worker_token}",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Inseminator.objects.filter(pk=inseminator.pk).exists()

    def test_delete_inseminator_as_regular_user_permission_denied(self):
        """
        Test deleting an inseminator as a regular user (permission denied).
        """
        serializer = InseminatorSerializer(data=self.inseminators_data)
        assert serializer.is_valid()
        inseminator = serializer.save()

        response = self.client.delete(
            reverse("dairy:inseminator-records-detail", kwargs={"pk": inseminator.pk}),
            HTTP_AUTHORIZATION=f"Token {self.regular_user_token}",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Inseminator.objects.filter(pk=inseminator.pk).exists()

    def test_delete_inseminator_without_authentication(self):
        """
        Test deleting an inseminator without authentication.
        """
        serializer = InseminatorSerializer(data=self.inseminators_data)
        assert serializer.is_valid()
        inseminator = serializer.save()

        response = self.client.delete(
            reverse("dairy:inseminator-records-detail", kwargs={"pk": inseminator.pk})
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert Inseminator.objects.filter(pk=inseminator.pk).exists()


@pytest.mark.django_db
class TestPregnancyViewSet:
    @pytest.fixture(autouse=True)
    def setup(self, setup_users, setup_pregnancy_data):
        self.client = setup_users['client']

        self.regular_user_token = setup_users['regular_user_token']
        self.farm_owner_token = setup_users['farm_owner_token']
        self.farm_manager_token = setup_users['farm_manager_token']
        self.asst_farm_manager_token = setup_users['asst_farm_manager_token']
        self.team_leader_token = setup_users['team_leader_token']
        self.farm_worker_token = setup_users['farm_worker_token']

        self.pregnancy_data = setup_pregnancy_data

    def test_add_pregnancy_as_farm_owner(self):
        """
        Test adding pregnancy record as a farm owner.
        """
        response = self.client.post(reverse("dairy:pregnancy-records-list"),
                                    data=self.pregnancy_data, format="json",
                                    HTTP_AUTHORIZATION=f'Token {self.farm_owner_token}')
        assert response.status_code == status.HTTP_201_CREATED
        assert Pregnancy.objects.filter(cow=self.pregnancy_data['cow']).exists()

    def test_add_pregnancy_as_farm_manager(self):
        """
        Test adding pregnancy record as a farm manager.
        """
        response = self.client.post(reverse("dairy:pregnancy-records-list"),
                                    data=self.pregnancy_data, format="json",
                                    HTTP_AUTHORIZATION=f'Token {self.farm_manager_token}')
        assert response.status_code == status.HTTP_201_CREATED
        assert Pregnancy.objects.filter(cow=self.pregnancy_data['cow']).exists()

    def test_add_pregnancy_as_assistant_farm_manager_permission_denied(self):
        """
        Test adding pregnancy record as an assistant farm manager (permission denied).
        """
        response = self.client.post(reverse("dairy:pregnancy-records-list"),
                                    data=self.pregnancy_data, format="json",
                                    HTTP_AUTHORIZATION=f'Token {self.asst_farm_manager_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_add_pregnancy_as_team_leader_permission_denied(self):
        """
        Test adding pregnancy record as a team leader (permission denied).
        """
        response = self.client.post(reverse("dairy:pregnancy-records-list"),
                                    data=self.pregnancy_data, format="json",
                                    HTTP_AUTHORIZATION=f'Token {self.team_leader_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_add_pregnancy_as_farm_worker_permission_denied(self):
        """
        Test adding pregnancy record as a farm worker (permission denied).
        """
        response = self.client.post(reverse("dairy:pregnancy-records-list"),
                                    data=self.pregnancy_data, format="json",
                                    HTTP_AUTHORIZATION=f'Token {self.farm_worker_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_add_pregnancy_as_regular_user_permission_denied(self):
        """
        Test adding pregnancy record as a regular user (permission denied).
        """
        response = self.client.post(reverse("dairy:pregnancy-records-list"),
                                    data=self.pregnancy_data, format="json",
                                    HTTP_AUTHORIZATION=f'Token {self.regular_user_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_add_pregnancy_unauthorized(self):
        """
        Test adding pregnancy record without authentication (unauthorized).
        """
        response = self.client.post(reverse("dairy:pregnancy-records-list"),
                                    data=self.pregnancy_data, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_view_pregnancy_as_farm_owner(self):
        """
        Test viewing pregnancy records as a farm owner.
        """
        response = self.client.get(reverse("dairy:pregnancy-records-list"),
                                   format="json",
                                   HTTP_AUTHORIZATION=f'Token {self.farm_owner_token}')
        assert response.status_code == status.HTTP_200_OK

    def test_view_pregnancy_as_farm_manager(self):
        """
        Test viewing pregnancy records as a farm manager.
        """
        response = self.client.get(reverse("dairy:pregnancy-records-list"),
                                   format="json",
                                   HTTP_AUTHORIZATION=f'Token {self.farm_manager_token}')
        assert response.status_code == status.HTTP_200_OK

    def test_view_pregnancy_as_assistant_farm_manager(self):
        """
        Test viewing pregnancy records as an assistant farm manager.
        """
        response = self.client.get(reverse("dairy:pregnancy-records-list"),
                                   format="json",
                                   HTTP_AUTHORIZATION=f'Token {self.asst_farm_manager_token}')
        assert response.status_code == status.HTTP_200_OK

    def test_view_pregnancy_as_team_leader(self):
        """
        Test viewing pregnancy records as a team leader.
        """
        response = self.client.get(reverse("dairy:pregnancy-records-list"),
                                   format="json",
                                   HTTP_AUTHORIZATION=f'Token {self.team_leader_token}')
        assert response.status_code == status.HTTP_200_OK

    def test_view_pregnancy_as_farm_worker(self):
        """
        Test viewing pregnancy records as a farm worker.
        """
        response = self.client.get(reverse("dairy:pregnancy-records-list"),
                                   format="json",
                                   HTTP_AUTHORIZATION=f'Token {self.farm_worker_token}')
        assert response.status_code == status.HTTP_200_OK

    def test_view_pregnancy_as_regular_user_permission_denied(self):
        """
        Test viewing pregnancy record as a regular user (permission denied).
        """
        response = self.client.get(reverse("dairy:pregnancy-records-list"),
                                   HTTP_AUTHORIZATION=f'Token {self.regular_user_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_view_pregnancy_unauthorized(self):
        """
        Test viewing pregnancy record without authentication (unauthorized).
        """
        response = self.client.get(reverse("dairy:pregnancy-records-list"))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_pregnancy_as_farm_owner(self):
        """
        Test updating pregnancy records as a farm owner.
        """
        serializer = PregnancySerializer(data=self.pregnancy_data)
        assert serializer.is_valid()
        pregnancy = serializer.save()
        update_data = {
            "pregnancy_status": PregnancyStatusChoices.FAILED,
            "pregnancy_notes": "Updated pregnancy status as failed",
            "pregnancy_failed_date": todays_date - timedelta(days=700)
        }
        response = self.client.patch(reverse("dairy:pregnancy-records-detail", kwargs={"pk": pregnancy.id}),
                                     data=update_data, format="json",
                                     HTTP_AUTHORIZATION=f'Token {self.farm_owner_token}')
        assert response.status_code == status.HTTP_200_OK
        assert Pregnancy.objects.get(id=pregnancy.id).pregnancy_status == update_data['pregnancy_status']
        assert Pregnancy.objects.get(id=pregnancy.id).pregnancy_notes == update_data['pregnancy_notes']

    def test_update_pregnancy_as_farm_manager(self):
        """
        Test updating pregnancy records as a farm manager.
        """
        serializer = PregnancySerializer(data=self.pregnancy_data)
        assert serializer.is_valid()
        pregnancy = serializer.save()
        update_data = {
            "pregnancy_status": PregnancyStatusChoices.FAILED,
            "pregnancy_notes": "Updated pregnancy status as failed",
            "pregnancy_failed_date": todays_date - timedelta(days=100)
        }
        response = self.client.patch(reverse("dairy:pregnancy-records-detail", kwargs={"pk": pregnancy.id}),
                                     data=update_data, format="json",
                                     HTTP_AUTHORIZATION=f'Token {self.farm_manager_token}')
        assert response.status_code == status.HTTP_200_OK
        assert Pregnancy.objects.get(id=pregnancy.id).pregnancy_status == update_data['pregnancy_status']
        assert Pregnancy.objects.get(id=pregnancy.id).pregnancy_notes == update_data['pregnancy_notes']

    def test_update_pregnancy_as_assistant_farm_manager(self):
        """
        Test updating pregnancy records as an assistant farm manager.
        """
        serializer = PregnancySerializer(data=self.pregnancy_data)
        assert serializer.is_valid()
        pregnancy = serializer.save()
        update_data = {
            "pregnancy_status": PregnancyStatusChoices.FAILED,
            "pregnancy_notes": "Updated pregnancy status as failed",
            "pregnancy_failed_date": todays_date - timedelta(days=102)
        }
        response = self.client.patch(reverse("dairy:pregnancy-records-detail", kwargs={"pk": pregnancy.id}),
                                     data=update_data, format="json",
                                     HTTP_AUTHORIZATION=f'Token {self.asst_farm_manager_token}')
        assert response.status_code == status.HTTP_200_OK
        assert Pregnancy.objects.get(id=pregnancy.id).pregnancy_status == update_data['pregnancy_status']
        assert Pregnancy.objects.get(id=pregnancy.id).pregnancy_notes == update_data['pregnancy_notes']

    def test_update_pregnancy_as_team_leader_permission_denied(self):
        """
        Test updating pregnancy records as team leader(permission denied)
        """
        serializer = PregnancySerializer(data=self.pregnancy_data)
        assert serializer.is_valid()
        pregnancy = serializer.save()
        update_data = {
            "pregnancy_status": PregnancyStatusChoices.FAILED,
            "pregnancy_notes": "Updated pregnancy status as failed",
            "pregnancy_failed_date": todays_date - timedelta(days=100)
        }
        response = self.client.patch(reverse("dairy:pregnancy-records-detail", kwargs={"pk": pregnancy.id}),
                                     data=update_data, format="json",
                                     HTTP_AUTHORIZATION=f'Token {self.team_leader_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_pregnancy_as_farm_worker_permission_denied(self):
        """
        Test updating pregnancy records as farm worker (permission denied)
        """
        serializer = PregnancySerializer(data=self.pregnancy_data)
        assert serializer.is_valid()
        pregnancy = serializer.save()
        update_data = {
            "pregnancy_status": PregnancyStatusChoices.FAILED,
            "pregnancy_notes": "Updated pregnancy status as failed",
            "pregnancy_failed_date": todays_date - timedelta(days=100)
        }
        response = self.client.patch(reverse("dairy:pregnancy-records-detail", kwargs={"pk": pregnancy.id}),
                                     data=update_data, format="json",
                                     HTTP_AUTHORIZATION=f'Token {self.farm_worker_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_pregnancy_as_regular_user_permission_denied(self):
        """
        Test updating pregnancy records as regular user (permission denied)
        """
        serializer = PregnancySerializer(data=self.pregnancy_data)
        assert serializer.is_valid()
        pregnancy = serializer.save()
        update_data = {
            "pregnancy_status": PregnancyStatusChoices.FAILED,
            "pregnancy_notes": "Updated pregnancy status as failed",
            "pregnancy_failed_date": todays_date - timedelta(days=100)
        }
        response = self.client.patch(reverse("dairy:pregnancy-records-detail", kwargs={"pk": pregnancy.id}),
                                     data=update_data, format="json",
                                     HTTP_AUTHORIZATION=f'Token {self.regular_user_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_pregnancy_unauthorized(self):
        """
        Test updating pregnancy records by unauthorized request
        """
        serializer = PregnancySerializer(data=self.pregnancy_data)
        assert serializer.is_valid()
        pregnancy = serializer.save()
        update_data = {
            "pregnancy_status": PregnancyStatusChoices.FAILED,
            "pregnancy_notes": "Updated pregnancy status as failed",
            "pregnancy_failed_date": todays_date - timedelta(days=100)
        }
        response = self.client.patch(reverse("dairy:pregnancy-records-detail", kwargs={"pk": pregnancy.id}),
                                     data=update_data, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_pregnancy_as_farm_owner(self):
        """
        Test deleting pregnancy records as a farm owner
        """
        serializer = PregnancySerializer(data=self.pregnancy_data)
        assert serializer.is_valid()
        pregnancy = serializer.save()
        response = self.client.delete(reverse("dairy:pregnancy-records-detail", kwargs={"pk": pregnancy.id}),
                                      format="json",
                                      HTTP_AUTHORIZATION=f'Token {self.farm_owner_token}')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Pregnancy.objects.filter(id=pregnancy.id).exists()

    def test_delete_pregnancy_as_farm_manager(self):
        """
        Test deleting pregnancy records as a farm manager
        """
        serializer = PregnancySerializer(data=self.pregnancy_data)
        assert serializer.is_valid()
        pregnancy = serializer.save()
        response = self.client.delete(reverse("dairy:pregnancy-records-detail", kwargs={"pk": pregnancy.id}),
                                      format="json",
                                      HTTP_AUTHORIZATION=f'Token {self.farm_manager_token}')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Pregnancy.objects.filter(id=pregnancy.id).exists()

    def test_delete_pregnancy_as_assistant_farm_manager_permission_denied(self):
        """
        Test deleting pregnancy records as an assistant farm manager (permission denied)
        """
        serializer = PregnancySerializer(data=self.pregnancy_data)
        assert serializer.is_valid()
        pregnancy = serializer.save()
        response = self.client.delete(reverse("dairy:pregnancy-records-detail", kwargs={"pk": pregnancy.id}),
                                      format="json",
                                      HTTP_AUTHORIZATION=f'Token {self.asst_farm_manager_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Pregnancy.objects.filter(id=pregnancy.id).exists()

    def test_delete_pregnancy_as_team_leader_permission_denied(self):
        """
        Test deleting pregnancy records as a team leader (permission denied)
        """
        serializer = PregnancySerializer(data=self.pregnancy_data)
        assert serializer.is_valid()
        pregnancy = serializer.save()
        response = self.client.delete(reverse("dairy:pregnancy-records-detail", kwargs={"pk": pregnancy.id}),
                                      format="json",
                                      HTTP_AUTHORIZATION=f'Token {self.team_leader_token}'
                                      )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Pregnancy.objects.filter(id=pregnancy.id).exists()

    def test_delete_pregnancy_as_farm_worker_permission_denied(self):
        """
        Test deleting pregnancy records as a farm worker (permission denied)
        """
        serializer = PregnancySerializer(data=self.pregnancy_data)
        assert serializer.is_valid()
        pregnancy = serializer.save()
        response = self.client.delete(reverse("dairy:pregnancy-records-detail", kwargs={"pk": pregnancy.id}),
                                      format="json",
                                      HTTP_AUTHORIZATION=f'Token {self.farm_worker_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Pregnancy.objects.filter(id=pregnancy.id).exists()

    def test_delete_pregnancy_as_regular_user_permission_denied(self):
        """
        Test deleting pregnancy records as a regular user (permission denied)
        """
        serializer = PregnancySerializer(data=self.pregnancy_data)
        assert serializer.is_valid()
        pregnancy = serializer.save()
        response = self.client.delete(reverse("dairy:pregnancy-records-detail", kwargs={"pk": pregnancy.id}),
                                      format="json",
                                      HTTP_AUTHORIZATION=f'Token {self.regular_user_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Pregnancy.objects.filter(id=pregnancy.id).exists()

    def test_delete_pregnancy_unauthorized(self):
        """
        Test deleting pregnancy by unauthorized request."""
        serializer = PregnancySerializer(data=self.pregnancy_data)
        assert serializer.is_valid()
        pregnancy = serializer.save()
        response = self.client.delete(reverse("dairy:pregnancy-records-detail", kwargs={"pk": pregnancy.id}),
                                      format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert Pregnancy.objects.filter(id=pregnancy.id).exists()


@pytest.mark.django_db
class TestInseminationViewSet:
    @pytest.fixture(autouse=True)
    def setup(self, setup_users, setup_insemination_data):
        self.client = setup_users['client']

        self.regular_user_token = setup_users['regular_user_token']
        self.farm_owner_token = setup_users['farm_owner_token']
        self.farm_manager_token = setup_users['farm_manager_token']
        self.asst_farm_manager_token = setup_users['asst_farm_manager_token']
        self.team_leader_token = setup_users['team_leader_token']
        self.farm_worker_token = setup_users['farm_worker_token']

        self.insemination_data = setup_insemination_data

    def test_add_insemination_as_farm_owner(self):
        """
        Test adding insemination record as farm owner.
        """

        response = self.client.post(reverse("dairy:insemination-records-list"), data=self.insemination_data,
                                    format="json", HTTP_AUTHORIZATION=f'Token {self.farm_owner_token}')
        assert response.status_code == status.HTTP_201_CREATED
        assert Insemination.objects.filter(cow=self.insemination_data['cow']).exists()

    def test_add_insemination_as_farm_manager(self):
        """
        Test adding insemination record as farm manager.
        """
        response = self.client.post(reverse("dairy:insemination-records-list"), data=self.insemination_data,
                                    format="json", HTTP_AUTHORIZATION=f'Token {self.farm_manager_token}')
        assert response.status_code == status.HTTP_201_CREATED
        assert Insemination.objects.filter(cow=self.insemination_data['cow']).exists()

    def test_add_insemination_as_assistant_manager(self):
        """
        Test adding insemination record as assistant farm manager.
        """

        response = self.client.post(reverse("dairy:insemination-records-list"), data=self.insemination_data,
                                    format="json", HTTP_AUTHORIZATION=f'Token {self.asst_farm_manager_token}')
        assert response.status_code == status.HTTP_201_CREATED
        assert Insemination.objects.filter(cow=self.insemination_data['cow']).exists()

    def test_add_insemination_as_team_leader(self):
        """
        Test adding insemination record as a team leader.
        """
        response = self.client.post(reverse("dairy:insemination-records-list"), data=self.insemination_data,
                                    format="json", HTTP_AUTHORIZATION=f'Token {self.team_leader_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not Insemination.objects.filter(cow=self.insemination_data['cow']).exists()

    def test_add_insemination_as_farm_worker(self):
        """
        Test adding insemination record as a farm worker.
        """
        response = self.client.post(reverse("dairy:insemination-records-list"), data=self.insemination_data,
                                    format="json", HTTP_AUTHORIZATION=f'Token {self.farm_worker_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not Insemination.objects.filter(cow=self.insemination_data['cow']).exists()

    def test_add_insemination_as_regular_user(self):
        """
        Test adding insemination record as regular user.
        """
        response = self.client.post(reverse("dairy:insemination-records-list"), data=self.insemination_data,
                                    format="json", HTTP_AUTHORIZATION=f'Token {self.regular_user_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert not Insemination.objects.filter(cow=self.insemination_data['cow']).exists()

    def test_add_insemination_without_authentication(self):
        """
        Test adding insemination record without authentication (unauthorized).
        """
        response = self.client.post(reverse("dairy:insemination-records-list"),
                                    data=self.insemination_data, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert not Insemination.objects.filter(cow=self.insemination_data['cow']).exists()

    def test_view_insemination_as_farm_owner(self):
        """
        Test viewing insemination records as a farm owner.
        """
        response = self.client.get(reverse("dairy:insemination-records-list"),
                                   format="json", HTTP_AUTHORIZATION=f'Token {self.farm_owner_token}')
        assert response.status_code == status.HTTP_200_OK

    def test_view_insemination_as_farm_manager(self):
        """
        Test viewing insemination records as a farm manager.
        """
        response = self.client.get(reverse("dairy:insemination-records-list"),
                                   format="json", HTTP_AUTHORIZATION=f'Token {self.farm_manager_token}')
        assert response.status_code == status.HTTP_200_OK

    def test_view_insemination_as_assistant_manager(self):
        """
        Test viewing insemination records as an assistant farm manager.
        """
        response = self.client.get(reverse("dairy:insemination-records-list"),
                                   format="json", HTTP_AUTHORIZATION=f'Token {self.asst_farm_manager_token}')
        assert response.status_code == status.HTTP_200_OK

    def test_view_insemination_as_team_leader_permission_denied(self):
        """
        Test viewing insemination records as a team leader (permission denied).
        """
        response = self.client.get(reverse("dairy:insemination-records-list"),
                                   format="json", HTTP_AUTHORIZATION=f'Token {self.team_leader_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_view_insemination_as_farm_worker_permission_denied(self):
        """
        Test viewing insemination records as a farm worker (permission denied).
        """
        response = self.client.get(reverse("dairy:insemination-records-list"),
                                   format="json", HTTP_AUTHORIZATION=f'Token {self.farm_worker_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_view_insemination_as_regular_user_permission_denied(self):
        """
        Test viewing insemination records as a regular user (permission denied).
        """
        response = self.client.get(reverse("dairy:insemination-records-list"),
                                   format="json", HTTP_AUTHORIZATION=f'Token {self.regular_user_token}')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_view_insemination_without_authentication(self):
        """
        Test viewing insemination records without authentication (unauthorized).
        """
        response = self.client.get(reverse("dairy:insemination-records-list"), format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_insemination_as_farm_owner(self):
        """
        Test updating insemination record as a farm owner.
        """
        serializer = InseminationSerializer(data=self.insemination_data)
        assert serializer.is_valid()
        insemination = serializer.save()

        update_data = {
            "success": True,
            "notes": "Updated notes for insemination"
        }

        response = self.client.patch(reverse("dairy:insemination-records-detail", kwargs={"pk": insemination.id}),
                                     data=update_data, format="json",
                                     HTTP_AUTHORIZATION=f'Token {self.farm_owner_token}')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['success'] == update_data['success']
        assert response.data['notes'] == update_data['notes']
        assert Insemination.objects.get(id=insemination.id).success == update_data['success']
        assert Insemination.objects.get(id=insemination.id).notes == update_data['notes']
        # Ensure other fields remain unchanged
        assert response.data['cow'] == self.insemination_data['cow']
        assert response.data['inseminator'] == self.insemination_data['inseminator']

    def test_update_insemination_as_farm_manager(self):
        """
        Test updating insemination record as a farm manager.
        """
        serializer = InseminationSerializer(data=self.insemination_data)
        assert serializer.is_valid()
        insemination = serializer.save()

        update_data = {
            "success": True,
            "notes": "Updated notes for insemination"
        }

        response = self.client.patch(reverse("dairy:insemination-records-detail", kwargs={"pk": insemination.id}),
                                     data=update_data, format="json",
                                     HTTP_AUTHORIZATION=f'Token {self.farm_manager_token}')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['success'] == update_data['success']
        assert response.data['notes'] == update_data['notes']
        assert Insemination.objects.get(id=insemination.id).success == update_data['success']
        assert Insemination.objects.get(id=insemination.id).notes == update_data['notes']
        # Ensure other fields remain unchanged
        assert response.data['cow'] == self.insemination_data['cow']
        assert response.data['inseminator'] == self.insemination_data['inseminator']

    def test_update_insemination_as_asst_farm_manager(self):
        """
        Test updating insemination record as an assistant farm manager.
        """
        serializer = InseminationSerializer(data=self.insemination_data)
        assert serializer.is_valid()
        insemination = serializer.save()

        update_data = {
            "success": True,
            "notes": "Updated notes for insemination"
        }

        response = self.client.patch(reverse("dairy:insemination-records-detail", kwargs={"pk": insemination.id}),
                                     data=update_data, format="json",
                                     HTTP_AUTHORIZATION=f'Token {self.asst_farm_manager_token}')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['success'] == update_data['success']
        assert response.data['notes'] == update_data['notes']
        assert Insemination.objects.get(id=insemination.id).success == update_data['success']
        assert Insemination.objects.get(id=insemination.id).notes == update_data['notes']
        # Ensure other fields remain unchanged
        assert response.data['cow'] == self.insemination_data['cow']
        assert response.data['inseminator'] == self.insemination_data['inseminator']

    def test_update_insemination_as_team_leader_permission_denied(self):
        """
        Test updating insemination record as a team leader (permission denied).
        """
        serializer = InseminationSerializer(data=self.insemination_data)
        assert serializer.is_valid()
        insemination = serializer.save()

        update_data = {
            "success": True,
            "notes": "Updated notes for insemination"
        }

        response = self.client.patch(reverse("dairy:insemination-records-detail", kwargs={"pk": insemination.id}),
                                     data=update_data, format="json",
                                     HTTP_AUTHORIZATION=f'Token {self.team_leader_token}')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_insemination_as_farm_worker_permission_denied(self):
        """
        Test updating insemination record as a farm worker (permission denied).
        """
        serializer = InseminationSerializer(data=self.insemination_data)
        assert serializer.is_valid()
        insemination = serializer.save()

        update_data = {
            "success": True,
            "notes": "Updated notes for insemination"
        }

        response = self.client.patch(reverse("dairy:insemination-records-detail", kwargs={"pk": insemination.id}),
                                     data=update_data, format="json",
                                     HTTP_AUTHORIZATION=f'Token {self.farm_worker_token}')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_insemination_as_regular_user_permission_denied(self):
        """
        Test updating insemination record as a regular user (permission denied).
        """
        serializer = InseminationSerializer(data=self.insemination_data)
        assert serializer.is_valid()
        insemination = serializer.save()

        update_data = {
            "success": True,
            "notes": "Updated notes for insemination"
        }

        response = self.client.patch(reverse("dairy:insemination-records-detail", kwargs={"pk": insemination.id}),
                                     data=update_data, format="json",
                                     HTTP_AUTHORIZATION=f'Token {self.regular_user_token}')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_insemination_unauthorized(self):
        """
        Test updating insemination record without authentication (unauthorized).
        """
        serializer = InseminationSerializer(data=self.insemination_data)
        assert serializer.is_valid()
        insemination = serializer.save()

        update_data = {
            "success": True,
            "notes": "Updated notes for insemination"
        }

        response = self.client.patch(reverse("dairy:insemination-records-detail", kwargs={"pk": insemination.id}),
                                     data=update_data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_insemination_as_farm_owner(self):
        """
        Test deleting insemination record as a farm owner.
        """
        serializer = InseminationSerializer(data=self.insemination_data)
        assert serializer.is_valid()
        insemination = serializer.save()

        response = self.client.delete(reverse("dairy:insemination-records-detail", kwargs={"pk": insemination.id}),
                                      HTTP_AUTHORIZATION=f'Token {self.farm_owner_token}')

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_insemination_as_farm_manager(self):
        """
        Test deleting an insemination record as a farm manager.
        """
        serializer = InseminationSerializer(data=self.insemination_data)
        assert serializer.is_valid()
        insemination = serializer.save()

        response = self.client.delete(reverse("dairy:insemination-records-detail", kwargs={"pk": insemination.id}),
                                      HTTP_AUTHORIZATION=f'Token {self.farm_manager_token}')

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_insemination_as_asst_farm_manager(self):
        """
        Test deleting an insemination record as an assistant farm manager.
        """
        serializer = InseminationSerializer(data=self.insemination_data)
        assert serializer.is_valid()
        insemination = serializer.save()

        response = self.client.delete(reverse("dairy:insemination-records-detail", kwargs={"pk": insemination.id}),
                                      HTTP_AUTHORIZATION=f'Token {self.asst_farm_manager_token}')

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_insemination_as_team_leader_permission_denied(self):
        """
        Test deleting an insemination record as a team leader (permission denied).
        """
        serializer = InseminationSerializer(data=self.insemination_data)
        assert serializer.is_valid()
        insemination = serializer.save()

        response = self.client.delete(reverse("dairy:insemination-records-detail", kwargs={"pk": insemination.id}),
                                      HTTP_AUTHORIZATION=f'Token {self.team_leader_token}')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_insemination_as_farm_worker_permission_denied(self):
        """
        Test deleting an insemination record as a farm worker (permission denied).
        """
        serializer = InseminationSerializer(data=self.insemination_data)
        assert serializer.is_valid()
        insemination = serializer.save()

        response = self.client.delete(reverse("dairy:insemination-records-detail", kwargs={"pk": insemination.id}),
                                      HTTP_AUTHORIZATION=f'Token {self.farm_worker_token}')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_insemination_as_regular_user_permission_denied(self):
        """
        Test deleting an insemination record as a regular user (permission denied).
        """
        serializer = InseminationSerializer(data=self.insemination_data)
        assert serializer.is_valid()
        insemination = serializer.save()

        response = self.client.delete(reverse("dairy:insemination-records-detail", kwargs={"pk": insemination.id}),
                                      HTTP_AUTHORIZATION=f'Token {self.regular_user_token}')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_insemination_unauthorized(self):
        """
        Test deleting an insemination record without authentication (unauthorized).
        """
        serializer = InseminationSerializer(data=self.insemination_data)
        assert serializer.is_valid()
        insemination = serializer.save()

        response = self.client.delete(reverse("dairy:insemination-records-detail", kwargs={"pk": insemination.id}))

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_insemination_associated_with_pregnancy(self):
        """
        Test deleting an insemination record associated with a pregnancy.
        """
        self.insemination_data["success"] = True
        serializer = InseminationSerializer(data=self.insemination_data)
        assert serializer.is_valid()
        insemination = serializer.save()

        response = self.client.delete(reverse("dairy:insemination-records-detail", kwargs={"pk": insemination.id}),
                                      HTTP_AUTHORIZATION=f'Token {self.farm_manager_token}')
        assert "Deletion not allowed. Insemination record is associated with a pregnancy." in response.data['detail']

        assert response.status_code == status.HTTP_403_FORBIDDEN
