from django.urls import reverse
from rest_framework.test import APIRequestFactory, APITestCase

from poultry.views import *


class FlockSourceViewSetTestCase(APITestCase):
    def setUp(self):
        """
        Set up the test case by creating the APIRequestFactory, viewset, URLs,
        and test data for creating, listing, and deleting flock sources.

        """

        self.factory = APIRequestFactory()
        self.viewset = FlockSourceViewSet.as_view({
            'get': 'list',
            'post': 'create',
            'delete': 'destroy'
        })
        self.url = reverse('poultry:flock-sources-list')
        self.valid_data = {'source': FlockSourceChoices.THIS_FARM}
        self.invalid_data = {'source': 'Invalid Source'}

    def test_create_flock_source(self):
        """
        Test the create operation for a flock source.

        - Create a POST request with valid data.
        - Execute the create view with the request.
        - Check that the response status code is 201 (Created).
        - Check that a flock source is created with the expected data.

        """

        request = self.factory.post(self.url, self.valid_data)
        response = self.viewset(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(FlockSource.objects.count(), 1)
        self.assertEqual(FlockSource.objects.get().source, FlockSourceChoices.THIS_FARM)

    def test_list_flock_sources(self):
        """
        Test the list operation for flock sources.

        - Create two flock sources.
        - Create a GET request for the list URL.
        - Execute the list view with the request.
        - Check that the response status code is 200 (OK).
        - Compare the response data with the serialized flock sources.

        """

        FlockSource.objects.create(source=FlockSourceChoices.UZIMA_CHICKEN)
        FlockSource.objects.create(source=FlockSourceChoices.KIPLELS_FARM)

        request = self.factory.get(self.url)
        response = self.viewset(request)
        queryset = FlockSource.objects.all()
        serializer = FlockSourceSerializer(queryset, many=True)
        expected_data = serializer.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_data)
        self.assertEqual(FlockSource.objects.count(), 2)

    def test_create_invalid_flock_source(self):
        """
        Test the create operation with invalid data for a flock source.

        - Create a POST request with invalid data.
        - Execute the create view with the request.
        - Check that the response status code is 400 (Bad Request).
        - Check that no flock source is created.

        """

        request = self.factory.post(self.url, self.invalid_data)
        response = self.viewset(request)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(FlockSource.objects.count(), 0)

    def test_delete_flock_source(self):
        """
        Test the delete operation for a flock source.

        - Create a flock source.
        - Create a DELETE request for the specific flock source URL.
        - Execute the delete view with the request.
        - Check that the response status code is 204 (No Content).
        - Check that the flock source is deleted.

        """

        flock_source = FlockSource.objects.create(source=FlockSourceChoices.THIS_FARM)
        delete_url = reverse('poultry:flock-sources-detail', args=[flock_source.pk])

        request = self.factory.delete(delete_url)
        response = self.viewset(request, pk=flock_source.pk)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(FlockSource.objects.count(), 0)


class FlockBreedViewSetTestCase(APITestCase):
    def setUp(self):
        """
        Set up the test case by creating the APIRequestFactory, viewset, URLs,
        and test data for creating, listing, and deleting flock breeds.

        """

        self.factory = APIRequestFactory()
        self.viewset = FlockBreedViewSet.as_view({
            'get': 'list',
            'post': 'create',
            'delete': 'destroy'
        })
        self.url = reverse('poultry:flock-breeds-list')
        self.valid_data = {'name': FlockBreedTypeChoices.KUROILER}
        self.invalid_data = {'name': 'Invalid Source'}

    def test_create_flock_breed(self):
        """
        Test the create operation for a flock breed.

        - Create a POST request with valid data.
        - Execute the create view with the request.
        - Check that the response status code is 201 (Created).
        - Check that a flock breed is created with the expected data.

        """

        request = self.factory.post(self.url, self.valid_data)
        response = self.viewset(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(FlockBreed.objects.count(), 1)
        self.assertEqual(FlockBreed.objects.get().name, FlockBreedTypeChoices.KUROILER)

    def test_list_flock_breeds(self):
        """
        Test the list operation for flock breed.

        - Create two flock breeds.
        - Create a GET request for the list URL.
        - Execute the list view with the request.
        - Check that the response status code is 200 (OK).
        - Compare the response data with the serialized flock breeds.

        """

        FlockBreed.objects.create(name=FlockBreedTypeChoices.KUROILER)
        FlockBreed.objects.create(name=FlockBreedTypeChoices.BANTAM)

        request = self.factory.get(self.url)
        response = self.viewset(request)
        queryset = FlockBreed.objects.all()
        serializer = FlockBreedSerializer(queryset, many=True)
        expected_data = serializer.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_data)
        self.assertEqual(FlockBreed.objects.count(), 2)

    def test_create_invalid_flock_breed(self):
        """
        Test the create operation with invalid data for a flock breed.

        - Create a POST request with invalid data.
        - Execute the create view with the request.
        - Check that the response status code is 400 (Bad Request).
        - Check that no flock breed is created.

        """

        request = self.factory.post(self.url, self.invalid_data)
        response = self.viewset(request)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(FlockBreed.objects.count(), 0)

    def test_delete_flock_breed(self):
        """
        Test the delete operation for a flock breed.

        - Create a flock breed.
        - Create a DELETE request for the specific flock breed URL.
        - Execute the delete view with the request.
        - Check that the response status code is 204 (No Content).
        - Check that the flock breed is deleted.

        """

        flock_breed = FlockBreed.objects.create(name=FlockBreedTypeChoices.KUROILER)
        delete_url = reverse('poultry:flock-breeds-detail', kwargs={'pk': flock_breed.pk})

        request = self.factory.delete(delete_url)
        response = self.viewset(request, pk=flock_breed.pk)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(FlockBreed.objects.count(), 0)


class HousingStructureViewSetTestCase(APITestCase):
    def setUp(self):
        """
        Set up the test case by creating the APIRequestFactory, viewset, URLs,
        and test data for creating, listing, retrieving, updating, and deleting housing structures.

        """

        self.factory: APIRequestFactory = APIRequestFactory()
        self.viewset = HousingStructureViewSet.as_view({
            'get': 'list',
            'post': 'create',
            'delete': 'destroy',
            'put': 'update'
        })
        self.retrieve_viewset: HousingStructureViewSet = HousingStructureViewSet.as_view({'get': 'retrieve'})
        self.url: str = reverse('poultry:housing-structures-list')
        self.valid_data: dict = {
            'type': HousingStructureTypeChoices.DEEP_LITTER_HOUSE,
            'category': HousingStructureCategoryChoices.GROWERS_HOUSE
        }

    def test_create_housing_structure(self):
        """
        Test the create operation for a housing structure.

        - Create a POST request with valid data.
        - Execute the create view with the request.
        - Check that the response status code is 201 (Created).
        - Check that a housing structure is created with the expected data.

        """

        request = self.factory.post(self.url, self.valid_data)
        response = self.viewset(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(HousingStructure.objects.count(), 1)
        self.assertEqual(HousingStructure.objects.get().type, HousingStructureTypeChoices.DEEP_LITTER_HOUSE)
        self.assertEqual(HousingStructure.objects.get().category, HousingStructureCategoryChoices.GROWERS_HOUSE)

    def test_list_housing_structures(self):
        """
        Test the list operation for housing structures.

        - Create two housing structures.
        - Create a GET request for the list URL.
        - Execute the list view with the request.
        - Check that the response status code is 200 (OK).
        - Compare the response data with the serialized housing structures.

        """

        HousingStructure.objects.create(
            type=HousingStructureTypeChoices.DEEP_LITTER_HOUSE,
            category=HousingStructureCategoryChoices.GROWERS_HOUSE
        )
        HousingStructure.objects.create(
            type=HousingStructureTypeChoices.BATTERY_CAGE,
            category=HousingStructureCategoryChoices.BROILERS_HOUSE
        )

        request = self.factory.get(self.url)
        response = self.viewset(request)
        queryset = HousingStructure.objects.all()
        serializer = HousingStructureSerializer(queryset, many=True)
        expected_data = serializer.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)
        self.assertEqual(HousingStructure.objects.count(), 2)

    def test_retrieve_housing_structure(self):
        """
        Test the retrieve operation for a housing structure.

        - Create a housing structure.
        - Create a GET request for the specific housing structure URL.
        - Execute the retrieve view with the request.
        - Compare the response data with the serialized housing structure.

        """

        housing_structure: HousingStructure = HousingStructure.objects.create(
            type=HousingStructureTypeChoices.DEEP_LITTER_HOUSE,
            category=HousingStructureCategoryChoices.GROWERS_HOUSE
        )
        retrieve_url = reverse('poultry:housing-structures-detail', kwargs={'pk': housing_structure.pk})

        request = self.factory.get(retrieve_url)
        response = self.retrieve_viewset(request, pk=housing_structure.pk)

        serializer = HousingStructureSerializer(housing_structure)
        expected_data = serializer.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_update_housing_structure(self):
        """
        Test the update operation for a housing structure.

        - Create a housing structure.
        - Create a PUT request with updated data.
        - Execute the update view with the request.
        - Check that the response status code is 200 (OK).
        - Check that the housing structure is updated with the new data.

        """

        housing_structure: HousingStructure = HousingStructure.objects.create(
            type=HousingStructureTypeChoices.DEEP_LITTER_HOUSE,
            category=HousingStructureCategoryChoices.GROWERS_HOUSE
        )
        update_url = reverse('poultry:housing-structures-detail', kwargs={'pk': housing_structure.pk})
        updated_data = {
            'type': HousingStructureTypeChoices.BATTERY_CAGE,
            'category': HousingStructureCategoryChoices.BROILERS_HOUSE
        }

        request = self.factory.put(update_url, updated_data)
        response = self.viewset(request, pk=housing_structure.pk)

        housing_structure.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(housing_structure.type, HousingStructureTypeChoices.BATTERY_CAGE)
        self.assertEqual(housing_structure.category, HousingStructureCategoryChoices.BROILERS_HOUSE)

    def test_delete_housing_structure(self):
        """
        Test the delete operation for a housing structure.

        - Create a housing structure.
        - Create a DELETE request for the specific housing structure URL.
        - Execute the delete view with the request.
        - Check that the response status code is 204 (No Content).
        - Check that the housing structure is deleted.

        """

        housing_structure: HousingStructure = HousingStructure.objects.create(
            type=HousingStructureTypeChoices.DEEP_LITTER_HOUSE,
            category=HousingStructureCategoryChoices.GROWERS_HOUSE
        )
        delete_url = reverse('poultry:housing-structures-detail', kwargs={'pk': housing_structure.pk})

        request = self.factory.delete(delete_url)
        response = self.viewset(request, pk=housing_structure.pk)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(HousingStructure.objects.count(), 0)


class FlockViewSetTestCase(APITestCase):
    def setUp(self):
        """
        Set up the test case by creating the APIRequestFactory, viewset, URLs,
        and test data for creating, listing, retrieving, updating, and deleting flocks.

        """

        self.factory: APIRequestFactory = APIRequestFactory()
        self.viewset = FlockViewSet.as_view({
            'get': 'list',
            'post': 'create',
            'delete': 'destroy',
            'put': 'update'
        })
        self.retrieve_viewset = FlockViewSet.as_view({'get': 'retrieve'})
        self.url: str = reverse('poultry:flocks-list')
        self.valid_data: dict = {
            'source': FlockSource.objects.create(source=FlockSourceChoices.UZIMA_CHICKEN).pk,
            'breed': FlockBreed.objects.create(name=FlockBreedTypeChoices.KUROILER).pk,
            'date_of_hatching': date.today() - timezone.timedelta(weeks=4),
            'chicken_type': ChickenTypeChoices.BROILER,
            'initial_number_of_birds': 100,
            'current_rearing_method': RearingMethodChoices.DEEP_LITTER,
            'current_housing_structure': HousingStructure.objects.create(
                type=HousingStructureTypeChoices.DEEP_LITTER_HOUSE,
                category=HousingStructureCategoryChoices.BROILERS_HOUSE
            ).pk,
        }

    def test_create_flock(self):
        """
        Test the create operation for a flock.

        - Create a POST request with valid data.
        - Execute the create view with the request.
        - Check that the response status code is 201 (Created).
        - Check that a flock is created with the expected data.

        """

        request = self.factory.post(self.url, self.valid_data)
        response = self.viewset(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Flock.objects.count(), 1)
        self.assertEqual(Flock.objects.get().chicken_type, ChickenTypeChoices.BROILER)

    def test_list_flocks(self):
        """
        Test the list operation for flocks.

        - Create a flock.
        - Create a GET request for the list URL.
        - Execute the list view with the request.
        - Check that the response status code is 200 (OK).
        - Compare the response data with the serialized flocks.

        """

        Flock.objects.create(
            source=FlockSource.objects.create(source=FlockSourceChoices.THIS_FARM),
            breed=FlockBreed.objects.create(name=FlockBreedTypeChoices.KUROILER),
            date_of_hatching=date.today() - timezone.timedelta(weeks=8),
            chicken_type=ChickenTypeChoices.LAYERS,
            initial_number_of_birds=200,
            current_rearing_method=RearingMethodChoices.BARN_SYSTEM,
            current_housing_structure=HousingStructure.objects.create(
                type=HousingStructureTypeChoices.CLOSED_SHED,
                category=HousingStructureCategoryChoices.BROODER_CHICK_HOUSE
            ),
        )

        request = self.factory.get(self.url)
        response = self.viewset(request)
        queryset = Flock.objects.all()
        serializer = FlockSerializer(queryset, many=True)
        expected_data = serializer.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)
        self.assertEqual(Flock.objects.count(), 1)

    def test_retrieve_flock(self):
        """
        Test the retrieve operation for a flock.

        - Create a flock.
        - Create a GET request for the specific flock URL.
        - Execute the retrieve view with the request.
        - Check that the response status code is 200 (OK).
        - Compare the response data with the serialized flock.

        """

        flock = Flock.objects.create(
            source=FlockSource.objects.create(source=FlockSourceChoices.KUKU_CHICK),
            breed=FlockBreed.objects.create(name=FlockBreedTypeChoices.KUROILER),
            date_of_hatching=date.today() - timezone.timedelta(weeks=10),
            chicken_type=ChickenTypeChoices.LAYERS,
            initial_number_of_birds=250,
            current_rearing_method=RearingMethodChoices.BARN_SYSTEM,
            current_housing_structure=HousingStructure.objects.create(
                type=HousingStructureTypeChoices.PASTURE_HOUSING,
                category=HousingStructureCategoryChoices.GROWERS_HOUSE
            ),
            date_established=date.today() - timezone.timedelta(weeks=10)
        )
        retrieve_url = reverse('poultry:flocks-detail', kwargs={'pk': flock.pk})

        request = self.factory.get(retrieve_url)
        response = self.retrieve_viewset(request, pk=flock.pk)

        serializer = FlockSerializer(flock)
        expected_data = serializer.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_update_flock(self):
        """
        Test the update operation for a flock.

        - Create a flock.
        - Create a PUT request with updated data.
        - Execute the update view with the request.
        - Check that the response status code is 200 (OK).
        - Check that the flock is updated with the new data.

        """

        flock = Flock.objects.create(
            source=FlockSource.objects.create(source=FlockSourceChoices.KIPLELS_FARM),
            breed=FlockBreed.objects.create(name=FlockBreedTypeChoices.KUROILER),
            date_of_hatching=date.today() - timezone.timedelta(weeks=6),
            chicken_type=ChickenTypeChoices.MULTI_PURPOSE,
            initial_number_of_birds=180,
            current_rearing_method=RearingMethodChoices.FREE_RANGE,
            current_housing_structure=HousingStructure.objects.create(
                type=HousingStructureTypeChoices.CLOSED_SHED,
                category=HousingStructureCategoryChoices.GROWERS_HOUSE
            )
        )
        update_url = reverse('poultry:flocks-detail', kwargs={'pk': flock.pk})
        updated_data = {
            'current_housing_structure': HousingStructure.objects.create(
                type=HousingStructureTypeChoices.OPEN_SIDED_SHED,
                category=HousingStructureCategoryChoices.LAYERS_HOUSE
            ).pk
        }

        request = self.factory.put(update_url, updated_data)
        response = self.viewset(request, pk=flock.pk)

        flock.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(flock.chicken_type, ChickenTypeChoices.MULTI_PURPOSE)
        self.assertEqual(flock.current_housing_structure.category, HousingStructureCategoryChoices.LAYERS_HOUSE)

    def test_delete_flock(self):
        """
        Test the delete operation for a flock.

        - Create a flock.
        - Create a DELETE request for the specific flock URL.
        - Execute the delete view with the request.
        - Check that the response status code is 204 (No Content).
        - Check that the flock is deleted.

        """

        flock = Flock.objects.create(
            source=FlockSource.objects.create(source=FlockSourceChoices.UZIMA_CHICKEN),
            breed=FlockBreed.objects.create(name=FlockBreedTypeChoices.KUROILER),
            date_of_hatching=date.today() - timezone.timedelta(weeks=4),
            chicken_type=ChickenTypeChoices.BROILER,
            initial_number_of_birds=120,
            current_rearing_method=RearingMethodChoices.DEEP_LITTER,
            current_housing_structure=HousingStructure.objects.create(
                type=HousingStructureTypeChoices.PASTURE_HOUSING,
                category=HousingStructureCategoryChoices.BROILERS_HOUSE
            ),
        )
        delete_url = reverse('poultry:flocks-detail', kwargs={'pk': flock.pk})

        request = self.factory.delete(delete_url)
        response = self.viewset(request, pk=flock.pk)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Flock.objects.count(), 0)

    def test_update_chicken_type_same_value(self):
        """
        Test updating the chicken type with the same value.

        - Create a flock.
        - Create a PUT request with updated data.
        - Execute the update view with the request.
        - Check that the response status code is 200 (OK).
        - Check that the flock is updated with the new data.

        """

        flock = Flock.objects.create(
            source=FlockSource.objects.create(source=FlockSourceChoices.KIPLELS_FARM),
            breed=FlockBreed.objects.create(name=FlockBreedTypeChoices.KUROILER),
            date_of_hatching=date.today() - timezone.timedelta(weeks=6),
            chicken_type=ChickenTypeChoices.MULTI_PURPOSE,
            initial_number_of_birds=180,
            current_rearing_method=RearingMethodChoices.FREE_RANGE,
            current_housing_structure=HousingStructure.objects.create(
                type=HousingStructureTypeChoices.CLOSED_SHED,
                category=HousingStructureCategoryChoices.GROWERS_HOUSE
            )
        )
        update_url = reverse('poultry:flocks-detail', kwargs={'pk': flock.pk})
        updated_data = {
            'chicken_type': ChickenTypeChoices.MULTI_PURPOSE,
            'current_housing_structure': HousingStructure.objects.create(
                type=HousingStructureTypeChoices.OPEN_SIDED_SHED,
                category=HousingStructureCategoryChoices.LAYERS_HOUSE
            ).pk
        }

        request = self.factory.put(update_url, updated_data)
        response = self.viewset(request, pk=flock.pk)

        flock.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(flock.chicken_type, ChickenTypeChoices.MULTI_PURPOSE)
        self.assertEqual(flock.current_housing_structure.category, HousingStructureCategoryChoices.LAYERS_HOUSE)

    def test_update_chicken_type_different_value(self):
        """
        Test updating the chicken type with a different value.

        - Create a flock.
        - Create a PUT request with updated data.
        - Execute the update view with the request.
        - Check that the response status code is 400 (Bad Request).

        """

        flock = Flock.objects.create(
            source=FlockSource.objects.create(source=FlockSourceChoices.KIPLELS_FARM),
            breed=FlockBreed.objects.create(name=FlockBreedTypeChoices.KUROILER),
            date_of_hatching=date.today() - timezone.timedelta(weeks=6),
            chicken_type=ChickenTypeChoices.MULTI_PURPOSE,
            initial_number_of_birds=180,
            current_rearing_method=RearingMethodChoices.FREE_RANGE,
            current_housing_structure=HousingStructure.objects.create(
                type=HousingStructureTypeChoices.CLOSED_SHED,
                category=HousingStructureCategoryChoices.GROWERS_HOUSE
            )
        )
        update_url = reverse('poultry:flocks-detail', kwargs={'pk': flock.pk})
        updated_data = {
            'chicken_type': ChickenTypeChoices.BROILER,
            'current_housing_structure': HousingStructure.objects.create(
                type=HousingStructureTypeChoices.OPEN_SIDED_SHED,
                category=HousingStructureCategoryChoices.LAYERS_HOUSE
            ).pk
        }

        request = self.factory.put(update_url, updated_data)
        response = self.viewset(request, pk=flock.pk)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(flock.chicken_type, ChickenTypeChoices.MULTI_PURPOSE)
        self.assertEqual(flock.current_housing_structure.category, HousingStructureCategoryChoices.GROWERS_HOUSE)


class FlockHistoryViewSetTestCase(APITestCase):
    """
    Test case for the FlockHistoryViewSet.

    This test case validates the behavior of the FlockHistoryViewSet endpoints.

    """

    def setUp(self):
        """
        Set up the necessary components for the test case.

        It creates a flock, flock history, and defines the URLs for the endpoints.

        """
        self.factory = APIRequestFactory()
        self.view_retrieve = FlockHistoryViewSet.as_view({'get': 'retrieve'})
        self.view_list = FlockHistoryViewSet.as_view({'get': 'list'})

        self.flock = Flock.objects.create(
            source=FlockSource.objects.create(source=FlockSourceChoices.KIPLELS_FARM),
            breed=FlockBreed.objects.create(name=FlockBreedTypeChoices.KUROILER),
            date_of_hatching=date.today() - timezone.timedelta(weeks=6),
            chicken_type=ChickenTypeChoices.MULTI_PURPOSE,
            initial_number_of_birds=180,
            current_rearing_method=RearingMethodChoices.FREE_RANGE,
            current_housing_structure=HousingStructure.objects.create(
                type=HousingStructureTypeChoices.CLOSED_SHED,
                category=HousingStructureCategoryChoices.GROWERS_HOUSE
            )
        )

        self.flock_history = FlockHistory.objects.filter(flock=self.flock).first()

        self.url_retrieve = reverse('poultry:flock-histories-detail', kwargs={'pk': self.flock.pk})
        self.url_list = reverse('poultry:flock-histories-list')

    def test_get_flock_history_detail(self):
        """
        Test the 'retrieve' endpoint of the FlockHistoryViewSet.

        - Create a GET request for the flock history detail.
        - Execute the retrieve view with the request.
        - Check that the response status code is 200 (OK).
        - Check that the response data matches the serialized flock history data.

        """
        request = self.factory.get(self.url_retrieve)
        response = self.view_retrieve(request, pk=self.flock_history.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = FlockHistorySerializer(self.flock_history)
        response_data = response.data
        self.assertEqual(response_data, serializer.data)

    def test_get_pen_inventory_list(self):
        """
        Test the 'list' endpoint of the FlockHistoryViewSet.

        - Create a GET request for the pen inventory list.
        - Execute the list view with the request.
        - Check that the response status code is 200 (OK).
        - Check that the response data matches the serialized flock history data.

        """
        request = self.factory.get(self.url_list)
        response = self.view_list(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = FlockHistorySerializer(FlockHistory.objects.all(), many=True)
        response_data = response.data
        self.assertEqual(response_data, serializer.data)


class FlockMovementViewSetTestCase(APITestCase):
    """
    Test case for the FlockMovementViewSet.

    This test case validates the behavior of the FlockMovementViewSet endpoints.

    """

    def setUp(self):
        """
        Set up the necessary objects for the test.

        It creates a flock, housing structures, and a flock movement.

        """

        self.factory = APIRequestFactory()
        self.view = FlockMovementViewSet.as_view(
            {'get': 'list', 'post': 'create', 'put': 'update', 'delete': 'destroy'})
        self.url = reverse('poultry:flock-movements-list')

        # Create a flock for testing
        flock_source = FlockSource.objects.create(source=FlockSourceChoices.THIS_FARM)
        self.from_structure = HousingStructure.objects.create(
            type=HousingStructureTypeChoices.SEMI_INTENSIVE_HOUSING,
            category=HousingStructureCategoryChoices.BROILERS_HOUSE,
        )
        self.to_structure = HousingStructure.objects.create(
            type=HousingStructureTypeChoices.SEMI_INTENSIVE_HOUSING,
            category=HousingStructureCategoryChoices.BROILERS_HOUSE,
        )
        self.to_structure_2 = HousingStructure.objects.create(
            type=HousingStructureTypeChoices.SEMI_INTENSIVE_HOUSING,
            category=HousingStructureCategoryChoices.BROILERS_HOUSE,
        )
        self.flock = Flock.objects.create(
            source=flock_source,
            breed=FlockBreed.objects.create(name=FlockBreedTypeChoices.KUROILER),
            date_of_hatching=timezone.now() - timedelta(weeks=4),
            chicken_type=ChickenTypeChoices.BROILER,
            initial_number_of_birds=100,
            current_rearing_method=RearingMethodChoices.CAGE_SYSTEM,
            current_housing_structure=self.from_structure,
        )

    def test_flock_movement_list(self):
        """
        Test the 'list' endpoint of the FlockMovementViewSet.

        - Create a GET request to the flock movements list URL.
        - Execute the list view with the request.
        - Check that the response status code is 200 (OK).

        """

        request = self.factory.get(self.url)
        response = self.view(request)
        self.assertEqual(response.status_code, 200)

    def test_flock_movement_create(self):
        """
        Test the 'create' endpoint of the FlockMovementViewSet.

        - Create a POST request with the necessary data.
        - Execute the create view with the request.
        - Check that the response status code is 201 (Created).
        - Check that the flock movement was created.

        """

        data = {
            'flock': self.flock.id,
            'from_structure': self.flock.current_housing_structure.id,
            'to_structure': self.to_structure.id,
        }
        request = self.factory.post(self.url, data)
        response = self.view(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(FlockMovement.objects.count(), 1)

        # Retrieve the updated flock from the database
        updated_flock = Flock.objects.get(id=self.flock.id)
        self.assertEqual(updated_flock.current_housing_structure, self.to_structure)

    def test_flock_movement_retrieve(self):
        """
        Test the 'retrieve' endpoint of the FlockMovementViewSet.

        - Create a GET request for a specific flock movement.
        - Execute the retrieve view with the request.
        - Check that the response status code is 200 (OK).

        """

        flock_movement = FlockMovement.objects.create(
            flock=self.flock,
            from_structure_id=self.from_structure.id,
            to_structure_id=self.to_structure.id
        )
        url = reverse('poultry:flock-movements-detail', kwargs={'pk': flock_movement.id})
        request = self.factory.get(url)
        response = self.view(request, pk=flock_movement.id)
        self.assertEqual(response.status_code, 200)

    def test_flock_movement_update(self):
        """
        Test the 'update' endpoint of the FlockMovementViewSet.

        - Create a PUT request with the necessary data.
        - Execute the update view with the request.
        - Check that the response status code is 200 (OK).
        - Check that the flock movement was updated.

        """

        flock_movement = FlockMovement.objects.create(
            flock=self.flock,
            from_structure_id=self.from_structure.id,
            to_structure_id=self.to_structure.id
        )
        url = reverse('poultry:flock-movements-detail', kwargs={'pk': flock_movement.id})
        data = {
            'flock': self.flock.id,
            'from_structure': self.flock.current_housing_structure.id,
            'to_structure': self.to_structure_2.id,
        }
        request = self.factory.put(url, data)
        response = self.view(request, pk=flock_movement.id)
        self.assertEqual(response.status_code, 200)

        # Retrieve the updated flock from the database
        updated_flock = Flock.objects.get(id=self.flock.id)
        self.assertEqual(updated_flock.current_housing_structure, self.to_structure_2)

    def test_flock_movement_delete(self):
        """
        Test the 'destroy' endpoint of the FlockMovementViewSet.

        - Create a DELETE request for a specific flock movement.
        - Execute the destroy view with the request.
        - Check that the response status code is 204 (No Content).
        - Check that the flock movement was deleted.

        """

        flock_movement = FlockMovement.objects.create(
            flock=self.flock,
            from_structure_id=self.from_structure.id,
            to_structure_id=self.to_structure.id
        )
        url = reverse('poultry:flock-movements-detail', kwargs={'pk': flock_movement.id})
        request = self.factory.delete(url)
        response = self.view(request, pk=flock_movement.id)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(FlockMovement.objects.count(), 0)


class FlockInspectionRecordViewSetTestCase(APITestCase):
    """
    Test case for the FlockInspectionRecordViewSet.

    This test case validates the behavior of the FlockInspectionRecordViewSet endpoints.

    """

    def setUp(self):
        """
        Set up the necessary objects for the test.

        It creates housing structures, a flock source, and a flock.

        """

        self.factory = APIRequestFactory()
        self.viewset = FlockInspectionRecordViewSet.as_view(
            {'get': 'list', 'post': 'create', 'put': 'update', 'delete': 'destroy'})
        self.viewset_retrieve = FlockInspectionRecordViewSet.as_view(
            {'get': 'retrieve'})
        self.url = reverse('poultry:flock-inspection-records-list')

        self.from_structure = HousingStructure.objects.create(
            type=HousingStructureTypeChoices.DEEP_LITTER_HOUSE,
            category=HousingStructureCategoryChoices.GROWERS_HOUSE
        )
        self.to_structure = HousingStructure.objects.create(
            type=HousingStructureTypeChoices.DEEP_LITTER_HOUSE,
            category=HousingStructureCategoryChoices.GROWERS_HOUSE
        )
        self.flock_source = FlockSource.objects.create(source=FlockSourceChoices.KIPLELS_FARM)
        self.flock = Flock.objects.create(
            source=self.flock_source,
            breed=FlockBreed.objects.create(name=FlockBreedTypeChoices.KUROILER),
            date_of_hatching=date.today() - timedelta(weeks=9),
            chicken_type=ChickenTypeChoices.LAYERS,
            initial_number_of_birds=100,
            current_rearing_method=RearingMethodChoices.CAGE_SYSTEM,
            current_housing_structure=self.from_structure,
        )

    def test_list_records(self):
        """
        Test the 'list' endpoint of the FlockInspectionRecordViewSet.

        - Create a GET request to the flock inspection records list URL.
        - Execute the list view with the request.
        - Retrieve all flock inspection records from the database.
        - Serialize the records.
        - Check that the response status code is 200 (OK).
        - Check that the response data matches the serialized records.

        """

        request = self.factory.get(self.url)
        response = self.viewset(request)
        records = FlockInspectionRecord.objects.all()
        serializer = FlockInspectionRecordSerializer(records, many=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_create_record(self):
        """
        Test the 'create' endpoint of the FlockInspectionRecordViewSet.

        - Create a POST request with the necessary data.
        - Execute the create view with the request.
        - Retrieve the last flock inspection record from the database.
        - Serialize the record.
        - Check that the response status code is 201 (Created).
        - Check that the response data matches the serialized record.

        """

        data = {
            'flock': self.flock.pk
        }

        request = self.factory.post(self.url, data)
        response = self.viewset(request)
        record = FlockInspectionRecord.objects.last()
        serializer = FlockInspectionRecordSerializer(record)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_record(self):
        """
        Test the 'retrieve' endpoint of the FlockInspectionRecordViewSet.

        - Create a GET request for a specific flock inspection record.
        - Execute the retrieve view with the request.
        - Retrieve the flock inspection record from the database.
        - Serialize the record.
        - Check that the response status code is 200 (OK).
        - Check that the response data matches the serialized record.

        """

        record = FlockInspectionRecord.objects.create(flock=self.flock)
        detail_url = reverse('poultry:flock-inspection-records-detail', kwargs={'pk': record.pk})
        request = self.factory.get(detail_url)
        response = self.viewset_retrieve(request, pk=record.pk)
        serializer = FlockInspectionRecordSerializer(record)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_update_record(self):
        """
        Test the 'update' endpoint of the FlockInspectionRecordViewSet.

        - Create a PUT request with the necessary data.
        - Execute the update view with the request.
        - Retrieve the updated flock inspection record from the database.
        - Serialize the record.
        - Check that the response status code is 200 (OK).
        - Check that the response data matches the serialized record.

        """

        record = FlockInspectionRecord.objects.create(flock=self.flock)
        detail_url = reverse('poultry:flock-inspection-records-detail', kwargs={'pk': record.pk})
        data = {
            'flock': self.flock.pk,
            'number_of_dead_birds': 3
        }

        request = self.factory.put(detail_url, data)
        response = self.viewset(request, pk=record.pk)
        record = FlockInspectionRecord.objects.get(pk=record.pk)
        serializer = FlockInspectionRecordSerializer(record)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_delete_record(self):
        """
        Test the 'destroy' endpoint of the FlockInspectionRecordViewSet.

        - Create a DELETE request for a specific flock inspection record.
        - Execute the destroy view with the request.
        - Check that the response status code is 204 (No Content).
        - Check that the flock inspection record no longer exists in the database.

        """

        record = FlockInspectionRecord.objects.create(flock=self.flock)
        detail_url = reverse('poultry:flock-inspection-records-detail', kwargs={'pk': record.pk})
        request = self.factory.delete(detail_url)
        response = self.viewset(request, pk=record.pk)

        self.assertEqual(response.status_code, 204)
        self.assertFalse(FlockInspectionRecord.objects.filter(pk=record.pk).exists())


class FlockBreedInformationViewSetTestCase(APITestCase):
    """
    Test case for the FlockBreedInformationViewSet.

    """

    def setUp(self):
        """
        Set up the test case by creating the APIRequestFactory, viewset, URLs,
        and test data for listing, creating, retrieving, updating, and deleting flock breed information.

        """

        self.factory = APIRequestFactory()
        self.viewset = FlockBreedInformationViewSet.as_view(
            {'get': 'list',
             'post': 'create',
             'put': 'update',
             'delete': 'destroy'
             })
        self.retrieve_viewset = FlockBreedInformationViewSet.as_view({'get': 'retrieve'})
        self.url = reverse('poultry:flock-breed-information-list')
        self.breed: FlockBreed = FlockBreed.objects.create(name=FlockBreedTypeChoices.BANTAM)
        self.flock_breed_information: FlockBreedInformation = FlockBreedInformation.objects.create(
            breed=self.breed,
            chicken_type=ChickenTypeChoices.LAYERS,
            average_mature_weight_in_kgs=2.0,
            average_egg_production=200,
            maturity_age_in_weeks=18
        )

    def test_list_flock_breed_information(self):
        """
        Test the 'list' action of the FlockBreedInformationViewSet.

        - Create a GET request for the flock breed information list URL.
        - Execute the list view with the request.
        - Check that the response status code is 200 (OK).

        """

        request = self.factory.get(self.url)
        response = self.viewset(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_flock_breed_information(self):
        """
        Test the 'create' action of the FlockBreedInformationViewSet.

        - Create a POST request with valid data.
        - Execute the create view with the request.
        - Check that the response status code is 201 (Created).

        """

        data = {
            'breed': self.breed.pk,
            'chicken_type': ChickenTypeChoices.BROILER,
            'average_mature_weight_in_kgs': 2.5,
            # 'average_egg_production': 10,
            'maturity_age_in_weeks': 10
        }

        request = self.factory.post(self.url, data)
        response = self.viewset(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_flock_breed_information(self):
        """
        Test the 'retrieve' action of the FlockBreedInformationViewSet.

        - Create a GET request for the specific flock breed information URL.
        - Execute the retrieve view with the request.
        - Check that the response status code is 200 (OK).

        """

        url = reverse('poultry:flock-breed-information-detail', kwargs={'pk': self.flock_breed_information.pk})
        request = self.factory.get(url)
        response = self.retrieve_viewset(request, pk=self.flock_breed_information.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_flock_breed_information(self):
        """
        Test the 'update' action of the FlockBreedInformationViewSet.

        - Create a PUT request with updated data.
        - Execute the update view with the request.
        - Check that the response status code is 200 (OK).

        """

        data = {
            'breed': self.breed.pk,
            'chicken_type': ChickenTypeChoices.LAYERS,
            'average_mature_weight_in_kgs': 2.5,
            'average_egg_production': 150,
            'maturity_age_in_weeks': 18
        }

        url = reverse('poultry:flock-breed-information-detail', kwargs={'pk': self.flock_breed_information.pk})
        request = self.factory.put(url, data)
        response = self.viewset(request, pk=self.flock_breed_information.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_flock_breed_information(self):
        """
        Test the 'destroy' action of the FlockBreedInformationViewSet.

        - Create a DELETE request for the specific flock breed information URL.
        - Execute the destroy view with the request.
        - Check that the response status code is 204 (No Content).

        """

        url = reverse('poultry:flock-breed-information-detail', kwargs={'pk': self.flock_breed_information.pk})
        request = self.factory.delete(url)
        response = self.viewset(request, pk=self.flock_breed_information.pk)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class EggCollectionViewSetTestCase(APITestCase):
    """
    Test case for the EggCollectionViewSet.

    """

    def setUp(self):
        """
        Set up the test case by creating the APIRequestFactory, viewset, URLs,
        and test data for listing, creating, retrieving, updating, and deleting egg collections.

        """

        self.factory = APIRequestFactory()
        self.view = EggCollectionViewSet.as_view(
            {'get': 'list',
             'post': 'create',
             'put': 'update',
             'delete': 'destroy'})
        self.retrieve_view = EggCollectionViewSet.as_view({'get': 'retrieve'})
        self.url = reverse('poultry:egg-collection-list')

        self.flock_source: FlockSource = FlockSource.objects.create(source=FlockSourceChoices.KUKU_CHICK)
        self.flock_breed: FlockBreed = FlockBreed.objects.create(name=FlockBreedTypeChoices.SASSO_F1)

        self.growers_house: HousingStructure = HousingStructure.objects.create(
            type=HousingStructureTypeChoices.SEMI_INTENSIVE_HOUSING,
            category=HousingStructureCategoryChoices.GROWERS_HOUSE)
        # Create a test flock
        self.flock: Flock = Flock.objects.create(
            source=self.flock_source,
            breed=self.flock_breed,
            date_of_hatching=date.today() - timedelta(weeks=17),
            chicken_type=ChickenTypeChoices.LAYERS,
            initial_number_of_birds=20,
            current_rearing_method=RearingMethodChoices.CAGE_SYSTEM,
            current_housing_structure=self.growers_house)
        self.serializer_data = {
            'flock': self.flock.pk,
            'collected_eggs': 3,
            'broken_eggs': 2
        }

    def test_list_egg_collections(self):
        """
        Test the 'list' action of the EggCollectionViewSet.

        - Create a GET request for the egg collection list URL.
        - Execute the list view with the request.
        - Check that the response status code is 200 (OK).

        """

        request = self.factory.get(self.url)
        response = self.view(request)
        self.assertEqual(response.status_code, 200)

    def test_create_egg_collection(self):
        """
        Test the 'create' action of the EggCollectionViewSet.

        - Create a POST request with valid data.
        - Execute the create view with the request.
        - Check that the response status code is 201 (Created).
        - Check that an egg collection is created with the expected data.

        """

        # FlockInspectionRecord.objects.create(flock=self.flock, number_of_dead_birds=20)
        request = self.factory.post(self.url, data=self.serializer_data)
        response = self.view(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(EggCollection.objects.count(), 1)
        self.assertEqual(response.data['collected_eggs'], self.serializer_data['collected_eggs'])
        self.assertEqual(response.data['broken_eggs'], self.serializer_data['broken_eggs'])

    def test_retrieve_egg_collection(self):
        """
        Test the 'retrieve' action of the EggCollectionViewSet.

        - Create an egg collection with the serializer data.
        - Create a GET request for the specific egg collection URL.
        - Execute the retrieve view with the request.
        - Check that the response status code is 200 (OK).
        - Check that the retrieved egg collection matches the serializer data.

        """

        serializer = EggCollectionSerializer(data=self.serializer_data)
        serializer.is_valid()
        egg_collection = serializer.save()
        url = reverse('poultry:egg-collection-detail', kwargs={'pk': egg_collection.pk})
        request = self.factory.get(url)
        response = self.retrieve_view(request, pk=egg_collection.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['collected_eggs'], self.serializer_data['collected_eggs'])
        self.assertEqual(response.data['broken_eggs'], self.serializer_data['broken_eggs'])

    def test_update_egg_collection(self):
        """
        Test the 'update' action of the EggCollectionViewSet.

        - Create an egg collection with the serializer data.
        - Create a PUT request with updated data.
        - Execute the update view with the request.
        - Check that the response status code is 200 (OK).
        - Check that the updated egg collection matches the updated data.

        """

        serializer = EggCollectionSerializer(data=self.serializer_data)
        serializer.is_valid()
        egg_collection = serializer.save()
        updated_data = {
            'flock': self.flock.id,
            'collected_eggs': 8,
            'broken_eggs': 3
        }
        url = reverse('poultry:egg-collection-detail', kwargs={'pk': egg_collection.pk})
        request = self.factory.put(url, data=updated_data)
        response = self.view(request, pk=egg_collection.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(EggCollection.objects.count(), 1)
        self.assertEqual(response.data['collected_eggs'], updated_data['collected_eggs'])
        self.assertEqual(response.data['broken_eggs'], updated_data['broken_eggs'])

    def test_destroy_egg_collection(self):
        """
        Test the 'destroy' action of the EggCollectionViewSet.

        - Create an egg collection with the serializer data.
        - Create a DELETE request for the specific egg collection URL.
        - Execute the destroy view with the request.
        - Check that the response status code is 204 (No Content).
        - Check that the egg collection is deleted.

        """

        serializer = EggCollectionSerializer(data=self.serializer_data)
        serializer.is_valid()
        egg_collection = serializer.save()
        url = reverse('poultry:egg-collection-detail', kwargs={'pk': egg_collection.pk})
        request = self.factory.delete(url)
        response = self.view(request, pk=egg_collection.pk)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(EggCollection.objects.count(), 0)
