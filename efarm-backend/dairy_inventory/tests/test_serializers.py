from django.test import TestCase

from dairy_inventory.serializers import *


class CowInventorySerializerTestCase(TestCase):
    def setUp(self):
        """
        Set up the test case by creating two cows.

        """

        self.cow1: Cow = Cow.objects.create(
            name='Test Cow 1',
            breed=BreedChoices.Friesian,
            date_of_birth=date.today(),
            gender=SexChoices.Male,
            availability_status=CowAvailabilityChoices.Alive
        )
        self.cow2: Cow = Cow.objects.create(
            name='Test Cow 2',
            breed=BreedChoices.Jersey,
            date_of_birth=date.today(),
            gender=SexChoices.Female,
            availability_status=CowAvailabilityChoices.Alive
        )

    def test_serializer_data_matches_cow_inventory_data(self):
        """
        Test that the serialized data matches the cow inventory data.

        - Retrieve the latest cow inventory.
        - Serialize the cow inventory.
        - Compare the serialized data with the expected data.

        """

        # Retrieve the latest cow inventory
        cow_inventory: CowInventory = CowInventory.objects.latest('last_update')

        # Serialize the cow inventory
        serializer: CowInventorySerializer = CowInventorySerializer(instance=cow_inventory)
        serialized_data = serializer.data

        expected_data = {
            'id': cow_inventory.id,
            'total_number_of_cows': 2,
            'number_of_male_cows': 1,
            'number_of_female_cows': 1,
            'number_of_sold_cows': 0,
            'number_of_dead_cows': 0,
            'last_update': cow_inventory.last_update.astimezone().isoformat(),
        }

        # Compare the serialized data with the expected data
        self.assertDictEqual(serialized_data, expected_data)


class BarnInventorySerializerTestCase(TestCase):
    def setUp(self):
        """
        Set up the test case by creating a barn.

        """

        self.barn: Barn = Barn.objects.create(name='Test Barn', capacity=10)

    def test_serializer_data_matches_barn_inventory_data(self):
        """
        Test that the serialized data matches the barn inventory data.

        - Retrieve the barn inventory.
        - Serialize the barn inventory.
        - Compare the serialized data with the expected data.

        """

        barn_inventory: BarnInventory = BarnInventory.objects.get(barn=self.barn)
        serializer: BarnInventorySerializer = BarnInventorySerializer(instance=barn_inventory)
        serialized_data = serializer.data

        expected_data = {
            'id': barn_inventory.id,
            'barn': self.barn.id,
            'number_of_cows': barn_inventory.number_of_cows,
            'number_of_pens': barn_inventory.number_of_pens,
            'last_update': barn_inventory.last_update.astimezone().isoformat(),
        }

        self.assertDictEqual(serialized_data, expected_data)


class BarnInventoryHistorySerializerTestCase(TestCase):
    def setUp(self):
        """
        Set up the test case by creating barns, cow pens, a cow, and a cow movement.

        """

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

    def test_serializer_data(self):
        """
        Test that the serialized data matches the barn inventory history data.

        - Retrieve the barn inventory and barn inventory history.
        - Serialize the barn inventory history.
        - Compare the serialized data with the expected data.

        """

        barn_inventory: BarnInventory = BarnInventory.objects.get(barn=self.barn2)
        barn_inventory_history: BarnInventoryHistory = BarnInventoryHistory.objects.latest('timestamp')

        serializer: BarnInventoryHistorySerializer = BarnInventoryHistorySerializer(instance=barn_inventory_history)
        serialized_data = serializer.data

        expected_data = {
            'id': barn_inventory_history.id,
            'barn_inventory': barn_inventory.id,
            'number_of_cows': barn_inventory.number_of_cows,
            'timestamp': barn_inventory_history.timestamp.astimezone().isoformat(),
        }

        self.assertDictEqual(serialized_data, expected_data)
