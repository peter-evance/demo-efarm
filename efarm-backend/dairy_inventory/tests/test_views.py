from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory

from dairy_inventory.views import *


class CowInventoryViewSetTestCase(TestCase):
    def setUp(self):
        """
        Set up the test case by creating the APIRequestFactory, views, cow, cow inventory,
        and URLs for retrieve and list operations.

        """

        self.factory = APIRequestFactory()
        self.view_retrieve = CowInventoryViewSet.as_view({'get': 'retrieve'})
        self.view_list = CowInventoryViewSet.as_view({'get': 'list'})

        self.cow: Cow = Cow.objects.create(
            name='Test Cow',
            breed=BreedChoices.Jersey,
            date_of_birth=date.today(),
            gender=SexChoices.Male,
            availability_status=CowAvailabilityChoices.Alive
        )

        self.cow_inventory: CowInventory = CowInventory.objects.first()
        self.url_retrieve = reverse('dairy_inventory:cows-inventory-detail', args=[self.cow_inventory.pk])
        self.url_list = reverse('dairy_inventory:cows-inventory-list')

    def test_get_cow_inventory_detail(self):
        """
        Test the retrieve operation for cow inventory.

        - Create a GET request for the retrieve URL.
        - Execute the retrieve view with the request.
        - Check that the response status code is 200 (OK).
        - Compare the response data with the serialized cow inventory.


        """

        request = self.factory.get(self.url_retrieve)
        response = self.view_retrieve(request, pk=self.cow_inventory.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = CowInventorySerializer(self.cow_inventory)
        response_data = response.data
        self.assertEqual(response_data, serializer.data)

    def test_get_cow_inventory_list_method_not_allowed(self):
        """
        Test that the list operation is not allowed for cow inventory.

        - Create a GET request for the list URL.
        - Execute the list view with the request.
        - Check that the response status code is 405 (Method Not Allowed).

        """

        request = self.factory.get(self.url_list)
        response = self.view_list(request)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class CowInventoryUpdateHistoryViewSetTestCase(TestCase):
    def setUp(self):
        """
        Set up the test case by creating the APIRequestFactory, views, cows, cow inventory update history,
        and URLs for retrieve and list operations.

        """

        self.factory = APIRequestFactory()
        self.view_retrieve = CowInventoryUpdateHistoryViewSet.as_view({'get': 'retrieve'})
        self.view_list = CowInventoryUpdateHistoryViewSet.as_view({'get': 'list'})

        self.cow1: Cow = Cow.objects.create(
            name='Test Cow 1',
            breed=BreedChoices.Jersey,
            date_of_birth=date.today(),
            gender=SexChoices.Female,
            availability_status=CowAvailabilityChoices.Alive
        )

        self.cow2: Cow = Cow.objects.create(
            name='Test Cow 2',
            breed=BreedChoices.Jersey,
            date_of_birth=date.today(),
            gender=SexChoices.Male,
            availability_status=CowAvailabilityChoices.Alive
        )

        self.cow_inventory_update_history: CowInventoryUpdateHistory = CowInventoryUpdateHistory.objects.first()
        self.url_retrieve = reverse('dairy_inventory:cow-inventory-history-detail',
                                    args=[self.cow_inventory_update_history.pk])
        self.url_list = reverse('dairy_inventory:cow-inventory-history-list')

    def test_get_cow_inventory_history_detail(self):
        """
        Test the retrieve operation for cow inventory update history.

        - Create a GET request for the retrieve URL.
        - Execute the retrieve view with the request.
        - Check that the response status code is 200 (OK).
        - Compare the response data with the serialized cow inventory update history.

        """

        request = self.factory.get(self.url_retrieve)
        response = self.view_retrieve(request, pk=self.cow_inventory_update_history.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = CowInventoryUpdateHistorySerializer(self.cow_inventory_update_history)
        response_data = response.data
        self.assertEqual(response_data, serializer.data)

    def test_get_cow_inventory_history_list(self):
        """
        Test the list operation for cow inventory update history.

        - Create a GET request for the list URL.
        - Execute the list view with the request.
        - Check that the response status code is 200 (OK).
        - Compare the response data with the serialized cow inventory update history.

        """

        request = self.factory.get(self.url_list)
        response = self.view_list(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = CowInventoryUpdateHistorySerializer(CowInventoryUpdateHistory.objects.all(), many=True)
        response_data = response.data
        self.assertEqual(response_data, serializer.data)


class CowPenInventoryViewSetTestCase(TestCase):
    def setUp(self):
        """
        Set up the test case by creating the APIRequestFactory, views, barn, pen, cow,
        pen inventory, and URLs for retrieve and list operations.

        """

        self.factory = APIRequestFactory()
        self.view_retrieve = CowPenInventoryViewSet.as_view({'get': 'retrieve'})
        self.view_list = CowPenInventoryViewSet.as_view({'get': 'list'})

        self.barn: Barn = Barn.objects.create(
            name='Test Barn',
            capacity=10
        )
        self.pen: CowPen = CowPen.objects.create(
            barn=self.barn,
            type=CowPenTypeChoices.Movable,
            category=CowPenCategoriesChoices.Calf_Pen,
            capacity=5
        )

        self.cow: Cow = Cow.objects.create(
            name='Test Cow',
            breed=BreedChoices.Jersey,
            date_of_birth=date.today(),
            gender=SexChoices.Male,
            availability_status=CowAvailabilityChoices.Alive
        )

        self.pen_inventory: CowPenInventory = CowPenInventory.objects.filter(pen=self.pen).first()

        self.url_retrieve = reverse('dairy_inventory:cow-pen-inventory-detail', args=[self.pen_inventory.pk])
        self.url_list = reverse('dairy_inventory:cow-pen-inventory-list')

    def test_get_pen_inventory_detail(self):
        """
        Test the retrieve operation for cow pen inventory.

        - Create a GET request for the retrieve URL.
        - Execute the retrieve view with the request.
        - Check that the response status code is 200 (OK).
        - Compare the response data with the serialized cow pen inventory.

        """

        request = self.factory.get(self.url_retrieve)
        response = self.view_retrieve(request, pk=self.pen_inventory.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = CowPenInventorySerializer(self.pen_inventory)
        response_data = response.data
        self.assertEqual(response_data, serializer.data)

    def test_get_pen_inventory_list(self):
        """
        Test the list operation for cow pen inventory.

        - Create a GET request for the list URL.
        - Execute the list view with the request.
        - Check that the response status code is 200 (OK).
        - Compare the response data with the serialized cow pen inventory.

        """

        request = self.factory.get(self.url_list)
        response = self.view_list(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = CowPenInventorySerializer(CowPenInventory.objects.all(), many=True)
        response_data = response.data
        self.assertEqual(response_data, serializer.data)


class CowPenHistoryViewSetTestCase(TestCase):
    def setUp(self):
        """
        Set up the test case by creating the APIRequestFactory, views, barn, pen,
        pen history, and URLs for retrieve and list operations.

        """

        self.factory = APIRequestFactory()
        self.view_retrieve = CowPenHistoryViewSet.as_view({'get': 'retrieve'})
        self.view_list = CowPenHistoryViewSet.as_view({'get': 'list'})

        self.barn: Barn = Barn.objects.create(
            name='Test Barn',
            capacity=10
        )
        self.pen: CowPen = CowPen.objects.create(
            barn=self.barn,
            type=CowPenTypeChoices.Movable,
            category=CowPenCategoriesChoices.Calf_Pen,
            capacity=5
        )

        self.pen_history: CowPenHistory = CowPenHistory.objects.filter(pen=self.pen).first()

        self.url_retrieve = reverse('dairy_inventory:cow-pen-history-detail', args=[self.pen_history.pk])
        self.url_list = reverse('dairy_inventory:cow-pen-history-list')

    def test_get_pen_history_detail(self):
        """
        Test the retrieve operation for cow pen history.

        - Create a GET request for the retrieve URL.
        - Execute the retrieve view with the request.
        - Check that the response status code is 200 (OK).
        - Compare the response data with the serialized cow pen history.

        """

        request = self.factory.get(self.url_retrieve)
        response = self.view_retrieve(request, pk=self.pen_history.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = CowPenHistorySerializer(self.pen_history)
        response_data = response.data
        self.assertEqual(response_data, serializer.data)

    def test_get_pen_history_list(self):
        """
        Test the list operation for cow pen history.

        - Create a GET request for the list URL.
        - Execute the list view with the request.
        - Check that the response status code is 200 (OK).
        - Compare the response data with the serialized cow pen history.

        """

        request = self.factory.get(self.url_list)
        response = self.view_list(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = CowPenHistorySerializer(CowPenHistory.objects.all(), many=True)
        response_data = response.data
        self.assertEqual(response_data, serializer.data)


class BarnInventoryViewSetTestCase(TestCase):
    def setUp(self):
        """
        Set up the test case by creating the APIRequestFactory, views, barn,
        barn inventory, and URLs for retrieve and list operations.

        """

        self.factory = APIRequestFactory()
        self.view_retrieve = BarnInventoryViewSet.as_view({'get': 'retrieve'})
        self.view_list = BarnInventoryViewSet.as_view({'get': 'list'})

        self.barn: Barn = Barn.objects.create(
            name='Test Barn',
            capacity=10
        )
        self.barn_inventory: BarnInventory = BarnInventory.objects.filter(barn=self.barn).first()

        self.url_retrieve = reverse('dairy_inventory:barn-inventory-cows-detail', args=[self.barn_inventory.pk])
        self.url_list = reverse('dairy_inventory:barn-inventory-cows-list')

    def test_get_barn_inventory_detail(self):
        """
        Test the retrieve operation for barn inventory.

        - Create a GET request for the retrieve URL.
        - Execute the retrieve view with the request.
        - Check that the response status code is 200 (OK).
        - Compare the response data with the serialized barn inventory.

        """

        request = self.factory.get(self.url_retrieve)
        response = self.view_retrieve(request, pk=self.barn_inventory.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = BarnInventorySerializer(self.barn_inventory)
        response_data = response.data
        self.assertEqual(response_data, serializer.data)

    def test_get_barn_inventory_list(self):
        """
        Test the list operation for barn inventory.

        - Create a GET request for the list URL.
        - Execute the list view with the request.
        - Check that the response status code is 200 (OK).
        - Compare the response data with the serialized barn inventory.

        """

        request = self.factory.get(self.url_list)
        response = self.view_list(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = BarnInventorySerializer(BarnInventory.objects.all(), many=True)
        response_data = response.data
        self.assertEqual(response_data, serializer.data)


class BarnInventoryHistoryViewSetTestCase(TestCase):
    def setUp(self):
        """
        Set up the test case by creating the APIRequestFactory, views, barns, pens, cow,
        barn inventory, barn inventory history, cow in pen movement, and URLs for
        retrieve and list operations.

        """

        self.factory = APIRequestFactory()
        self.view_retrieve = BarnInventoryHistoryViewSet.as_view({'get': 'retrieve'})
        self.view_list = BarnInventoryHistoryViewSet.as_view({'get': 'list'})

        self.barn1: Barn = Barn.objects.create(name='Test Barn 1', capacity=10)
        self.barn2: Barn = Barn.objects.create(name='Test Barn 2', capacity=10)
        self.pen1_barn: CowPen = CowPen.objects.create(
            barn=self.barn1,
            type=CowPenTypeChoices.Fixed,
            category=CowPenCategoriesChoices.Heifer_Pen,
            capacity=2
        )
        self.pen1_barn2: CowPen = CowPen.objects.create(
            barn=self.barn2,
            type=CowPenTypeChoices.Fixed,
            category=CowPenCategoriesChoices.General_Pen,
            capacity=2
        )
        self.cow: Cow = Cow.objects.create(
            name='Test Cow',
            breed=BreedChoices.Jersey,
            date_of_birth=date.today(),
            gender=SexChoices.Female,
            availability_status=CowAvailabilityChoices.Alive,
        )
        CowInPenMovement.objects.create(
            cow=self.cow,
            previous_pen=self.pen1_barn,
            new_pen=self.pen1_barn2
        )

        self.barn_inventory: BarnInventory = BarnInventory.objects.filter(barn=self.barn1).first()
        self.barn_inventory_history: BarnInventoryHistory = BarnInventoryHistory.objects.filter(
            barn_inventory=self.barn_inventory
        ).first()

        self.url_retrieve = reverse('dairy_inventory:barn-inventory-cows-history-detail',
                                    args=[self.barn_inventory_history.pk])
        self.url_list = reverse('dairy_inventory:barn-inventory-cows-history-list')

    def test_get_barn_inventory_history_detail(self):
        """
        Test the retrieve operation for barn inventory history.

        - Create a GET request for the retrieve URL.
        - Execute the retrieve view with the request.
        - Check that the response status code is 200 (OK).
        - Compare the response data with the serialized barn inventory history.

        """

        request = self.factory.get(self.url_retrieve)
        response = self.view_retrieve(request, pk=self.barn_inventory_history.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = BarnInventoryHistorySerializer(self.barn_inventory_history)
        response_data = response.data
        self.assertEqual(response_data, serializer.data)

    def test_get_barn_inventory_history_list(self):
        """
        Test the list operation for barn inventory history.

        - Create a GET request for the list URL.
        - Execute the list view with the request.
        - Check that the response status code is 200 (OK).
        - Compare the response data with the serialized barn inventory history.

        """

        request = self.factory.get(self.url_list)
        response = self.view_list(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = BarnInventoryHistorySerializer(BarnInventoryHistory.objects.all(), many=True)
        response_data = response.data
        self.assertEqual(response_data, serializer.data)
