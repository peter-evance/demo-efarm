from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIRequestFactory, APITestCase

from poultry.views import FlockMovementViewSet
from poultry_inventory.models import *
from poultry_inventory.views import *


class FlockInventoryViewSetTest(TestCase):
    """
    Test case for the FlockInventoryViewSet.

    This test case validates the behavior of the FlockInventoryViewSet endpoints.

    """

    def setUp(self):
        """
        Set up the necessary components for the test case.

        It creates a flock, flock inventory, and initializes the APIRequestFactory.

        """
        self.factory = APIRequestFactory()

        flock_source = FlockSource.objects.create(source=FlockSourceChoices.This_Farm)
        broiler_house = HousingStructure.objects.create(
            type=HousingStructureTypeChoices.Semi_Intensive_Housing,
            category=HousingStructureCategoryChoices.Broilers_House,
        )
        self.flock = Flock.objects.create(
            source=flock_source,
            date_of_hatching=timezone.now() - timedelta(weeks=4),
            chicken_type=ChickenTypeChoices.Broiler,
            initial_number_of_birds=100,
            current_rearing_method=RearingMethodChoices.Cage_System,
            current_housing_structure=broiler_house,
        )

        self.flock_inventory = FlockInventory.objects.get(flock=self.flock)

    def test_flock_inventory_list(self):
        """
        Test the 'list' endpoint of the FlockInventoryViewSet.

        It sends a GET request to the endpoint to retrieve the flock inventory list and verifies the response.

        """
        url = reverse('poultry_inventory:flock-inventories-list')
        request = self.factory.get(url)
        view = FlockInventoryViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_flock_inventory_retrieve(self):
        """
        Test the 'retrieve' endpoint of the FlockInventoryViewSet.

        It sends a GET request to the endpoint to retrieve the flock inventory detail and verifies the response.

        """
        url = reverse('poultry_inventory:flock-inventories-detail', kwargs={'pk': self.flock_inventory.id})
        request = self.factory.get(url)
        view = FlockInventoryViewSet.as_view({'get': 'retrieve'})
        response = view(request, pk=self.flock_inventory.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['flock'], self.flock_inventory.flock.id)


class FlockInventoryHistoryViewSetTest(TestCase):
    """
    Test case for the FlockInventoryHistoryViewSet.

    This test case validates the behavior of the FlockInventoryHistoryViewSet endpoints.

    """

    def setUp(self):
        """
        Set up the necessary components for the test case.

        It creates a flock, flock inventory, flock inventory history, and initializes the APIRequestFactory.

        """
        self.factory = APIRequestFactory()

        flock_source = FlockSource.objects.create(source=FlockSourceChoices.This_Farm)
        broiler_house = HousingStructure.objects.create(
            type=HousingStructureTypeChoices.Semi_Intensive_Housing,
            category=HousingStructureCategoryChoices.Broilers_House,
        )
        self.flock = Flock.objects.create(
            source=flock_source,
            date_of_hatching=timezone.now() - timedelta(weeks=4),
            chicken_type=ChickenTypeChoices.Broiler,
            initial_number_of_birds=100,
            current_rearing_method=RearingMethodChoices.Cage_System,
            current_housing_structure=broiler_house,
        )
        self.flock_inventory = FlockInventory.objects.get(flock=self.flock)
        self.flock_inventory_history = FlockInventoryHistory.objects.get(flock_inventory=self.flock_inventory)

    def test_flock_inventory_history_list(self):
        """
        Test the 'list' endpoint of the FlockInventoryHistoryViewSet.

        It sends a GET request to the endpoint to retrieve the flock inventory history list and verifies the response.

        """
        url = reverse('poultry_inventory:flock-inventory-histories-list')
        request = self.factory.get(url)
        view = FlockInventoryHistoryViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_flock_inventory_history_retrieve(self):
        """
        Test the 'retrieve' endpoint of the FlockInventoryHistoryViewSet.

        It sends a GET request to the endpoint to retrieve the flock inventory history detail and verifies the response.

        """
        url = reverse('poultry_inventory:flock-inventory-histories-detail', kwargs={'pk': self.flock_inventory_history.id})
        request = self.factory.get(url)
        view = FlockInventoryHistoryViewSet.as_view({'get': 'retrieve'})
        response = view(request, pk=self.flock_inventory_history.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['flock_inventory'], self.flock_inventory_history.flock_inventory.id)

