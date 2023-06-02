from typing import Callable

from django.http import HttpResponse
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory

from dairy.views import *


class CowPenViewSetTestCase(APITestCase):
    """
    Test case for the CowPenViewSet.

    This test case validates the behavior of the CowPenViewSet endpoints.

    """

    def setUp(self):
        """
        Set up the necessary objects for the test.

        It creates a barn and a cow pen.

        """
        self.factory: APIRequestFactory = APIRequestFactory()

        # Create barn object
        self.barn: Barn = Barn.objects.create(name='Barn 1', capacity=10)

        # Create cow pen objects
        self.pen: CowPen = CowPen.objects.create(
            barn=self.barn,
            type=CowPenTypeChoices.Movable,
            category=CowPenCategoriesChoices.Calf_Pen,
            capacity=5
        )

    def test_list_pens(self):
        """
        Test the 'list' endpoint of the CowPenViewSet.

        It sends a GET request to the endpoint and verifies the response.

        """
        url = reverse('dairy:cow-pen-list')
        request = self.factory.get(url)
        view: Callable[[APIView], HttpResponse]  = CowPenViewSet.as_view({'get': 'list'})
        response = view(request)
        serializer = CowPenSerializer(CowPen.objects.all(), many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_pen(self):
        """
        Test the 'retrieve' endpoint of the CowPenViewSet.

        It sends a GET request to the endpoint with a specific pen ID and verifies the response.

        """
        url = reverse('dairy:cow-pen-detail', kwargs={'pk': self.pen.pk})
        request = self.factory.get(url)
        view: Callable[[APIView], HttpResponse]  = CowPenViewSet.as_view({'get': 'retrieve'})
        response = view(request, pk=self.pen.pk)
        serializer = CowPenSerializer(self.pen)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_pen(self):
        """
        Test the 'create' endpoint of the CowPenViewSet.

        It sends a POST request to the endpoint with the necessary data and verifies the response.

        """
        url = reverse('dairy:cow-pen-list')
        data = {
            'barn': self.barn.pk,
            'type': 'Movable',
            'category': 'Calf Pen',
            'capacity': 9
        }
        request = self.factory.post(url, data)
        view: Callable[[APIView], HttpResponse] = CowPenViewSet.as_view({'post': 'create'})
        response = view(request)
        serializer = CowPenSerializer(CowPen.objects.last())

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)

    def test_update_pen(self):
        """
        Test the 'update' endpoint of the CowPenViewSet.

        It sends a PUT request to the endpoint with the necessary data and verifies the response.

        """
        url = reverse('dairy:cow-pen-detail', kwargs={'pk': self.pen.id})
        data = {
            'barn': self.barn.id,
            'type': 'Fixed',
            'category': 'Sick Pen',
            'capacity': 4
        }
        request = self.factory.put(url, data)
        view: Callable[[APIView], HttpResponse] = CowPenViewSet.as_view({'put': 'update'})
        response = view(request, pk=self.pen.pk)
        updated_pen: CowPen = CowPen.objects.get(pk=self.pen.pk)
        serializer = CowPenSerializer(updated_pen)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(updated_pen.capacity, 4)

    def test_delete_pen(self):
        """
        Test the 'destroy' endpoint of the CowPenViewSet.

        It sends a DELETE request to the endpoint with a specific pen ID and verifies the response.

        """
        url = reverse('dairy:cow-pen-detail', kwargs={'pk': self.pen.pk})
        request = self.factory.delete(url)
        view: Callable[[APIView], HttpResponse] = CowPenViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=self.pen.pk)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CowPen.objects.filter(id=self.pen.pk).exists())


class BarnViewSetTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.barn = Barn.objects.create(name='Barn 1', capacity=10)

    def test_list_barns(self):
        url = reverse('dairy:barn-list')
        request = self.factory.get(url)
        view = BarnViewSet.as_view({'get': 'list'})
        response = view(request)
        serializer = BarnSerializer(Barn.objects.all(), many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_barn(self):
        url = reverse('dairy:barn-detail', kwargs={'pk': self.barn.pk})
        request = self.factory.get(url)
        view = BarnViewSet.as_view({'get': 'retrieve'})
        response = view(request, pk=self.barn.pk)
        serializer = BarnSerializer(self.barn)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_barn(self):
        url = reverse('dairy:barn-list')
        data = {
            'name': 'New Barn',
            'capacity': 12
        }
        request = self.factory.post(url, data)
        view = BarnViewSet.as_view({'post': 'create'})
        response = view(request)
        serializer = BarnSerializer(Barn.objects.last())

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)

    def test_update_barn(self):
        url = reverse('dairy:barn-detail', kwargs={'pk': self.barn.pk})
        data = {
            'name': 'Updated Barn',
            'capacity': 20
        }
        request = self.factory.put(url, data)
        view = BarnViewSet.as_view({'put': 'update'})
        response = view(request, pk=self.barn.pk)
        updated_barn = Barn.objects.get(id=self.barn.pk)
        serializer = BarnSerializer(updated_barn)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(updated_barn.name, 'Updated Barn')
        self.assertEqual(updated_barn.capacity, 20)

    def test_delete_barn(self):
        url = reverse('dairy:barn-detail', kwargs={'pk': self.barn.pk})
        request = self.factory.delete(url)
        view = BarnViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=self.barn.pk)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Barn.objects.filter(id=self.barn.pk).exists())


class CowInBarnMovementViewSetTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

        # Create barns
        self.barn1 = Barn.objects.create(name='Barn 1', capacity=10)
        self.barn2 = Barn.objects.create(name='Barn 2', capacity=15)

        self.pen1_barn1 = CowPen.objects.create(
            barn=self.barn1,
            type=CowPenTypeChoices.Movable,
            category=CowPenCategoriesChoices.Sick_Pen,
            capacity=5
        )
        self.pen2_barn1 = CowPen.objects.create(
            barn=self.barn1,
            type=CowPenTypeChoices.Fixed,
            category=CowPenCategoriesChoices.Heifer_Pen,
            capacity=3
        )
        self.pen1_barn2 = CowPen.objects.create(
            barn=self.barn2,
            type=CowPenTypeChoices.Fixed,
            category=CowPenCategoriesChoices.Sick_Pen,
            capacity=9
        )
        # Create cows
        self.cow_1 = Cow.objects.create(
            name='Test Cow 1',
            breed=BreedChoices.Crossbreed,
            date_of_birth=date.today(),
            gender=SexChoices.Male,
            availability_status=CowAvailabilityChoices.Alive,
        )
        self.cow_2 = Cow.objects.create(
            name='Test Cow 2',
            breed=BreedChoices.Ayrshire,
            date_of_birth=date.today(),
            gender=SexChoices.Female,
            availability_status=CowAvailabilityChoices.Alive,
        )
        # Create cow in pen movements
        self.cow_in_pen_movement_1 = CowInPenMovement.objects.create(
            cow=self.cow_1,
            previous_pen=self.pen1_barn1,
            new_pen=self.pen2_barn1
        )
        self.cow_in_pen_movement_2 = CowInPenMovement.objects.create(
            cow=self.cow_2,
            previous_pen=self.pen1_barn1,
            new_pen=self.pen1_barn2
        )

    def test_list_cow_in_barn_movements(self):
        url = reverse('dairy:cow-in-barn-movement-list')
        request = self.factory.get(url)
        view = CowInBarnMovementViewSet.as_view({'get': 'list'})
        response = view(request)
        serializer = CowInBarnMovementSerializer(CowInBarnMovement.objects.all(), many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_cow_in_barn_movement(self):
        cow_in_barn_movement = CowInBarnMovement.objects.first()
        url = reverse('dairy:cow-in-barn-movement-detail', kwargs={'pk': cow_in_barn_movement.pk})
        request = self.factory.get(url)
        view = CowInBarnMovementViewSet.as_view({'get': 'retrieve'})
        response = view(request, pk=cow_in_barn_movement.pk)
        serializer = CowInBarnMovementSerializer(cow_in_barn_movement)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


class CowInPenMovementViewSetTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

        # Create barns
        self.barn1 = Barn.objects.create(name='Barn 1', capacity=10)

        # Create cow pens
        self.pen1 = CowPen.objects.create(
            barn=self.barn1,
            type=CowPenTypeChoices.Movable,
            category=CowPenCategoriesChoices.Sick_Pen,
            capacity=5
        )
        self.pen2 = CowPen.objects.create(
            barn=self.barn1,
            type=CowPenTypeChoices.Fixed,
            category=CowPenCategoriesChoices.Heifer_Pen,
            capacity=3
        )

        # Create cows
        self.cow = Cow.objects.create(
            name='Test Cow 1',
            breed=BreedChoices.Crossbreed,
            date_of_birth=date.today(),
            gender=SexChoices.Male,
            availability_status=CowAvailabilityChoices.Alive,
        )

    def test_list_cow_in_barn_movements(self):
        url = reverse('dairy:cow-in-pen-movement-list')
        request = self.factory.get(url)
        view = CowInPenMovementViewSet.as_view({'get': 'list'})
        response = view(request)
        serializer = CowInBarnMovementSerializer(CowInPenMovement.objects.all(), many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_cow_in_pen_movement(self):
        url = reverse('dairy:cow-in-pen-movement-list')
        data = {
            'cow': self.cow.pk,
            'previous_pen': self.pen1.pk,
            'new_pen': self.pen2.pk
        }
        request = self.factory.post(url, data)
        view = CowInPenMovementViewSet.as_view({'post': 'create'})
        response = view(request)
        serializer = CowInPenMovementSerializer(CowInPenMovement.objects.last())

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)
