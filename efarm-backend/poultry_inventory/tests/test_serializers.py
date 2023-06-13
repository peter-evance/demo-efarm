from datetime import timedelta

from django.test import TestCase
from poultry_inventory.models import *
from poultry_inventory.serializers import *


class FlockInventorySerializerTest(TestCase):
    """
    Test case for the FlockInventorySerializer.

    This test case verifies the creation of a flock inventory.

    """

    def setUp(self):
        """
        Set up the test case by creating a flock.

        """
        flock_source = FlockSource.objects.create(source=FlockSourceChoices.This_Farm)
        broiler_house = HousingStructure.objects.create(
            type=HousingStructureTypeChoices.Semi_Intensive_Housing,
            category=HousingStructureCategoryChoices.Broilers_House,
        )
        Flock.objects.create(
            source=flock_source,
            date_of_hatching=timezone.now() - timedelta(weeks=4),
            chicken_type=ChickenTypeChoices.Broiler,
            initial_number_of_birds=100,
            current_rearing_method=RearingMethodChoices.Cage_System,
            current_housing_structure=broiler_house,
        )
        self.flock = Flock.objects.all().first()

    def test_flock_inventory_creation(self):
        """
        Test the creation of a flock inventory.

        - Serialize the flock inventory.
        - Compare the serialized data with the expected data.

        """
        serializer = FlockInventorySerializer(instance=self.flock.inventory)
        self.assertEqual(serializer.data['flock'], self.flock.id)
        self.assertEqual(serializer.data['number_of_alive_birds'], self.flock.initial_number_of_birds)
        self.assertEqual(serializer.data['number_of_dead_birds'], 0)


class FlockInventoryHistorySerializerTest(TestCase):
    """
    Test case for the FlockInventoryHistorySerializer.

    This test case verifies the creation of a flock inventory history.

    """

    def setUp(self):
        """
        Set up the test case by creating a flock and its inventory.

        """
        flock_source = FlockSource.objects.create(source=FlockSourceChoices.This_Farm)
        broiler_house = HousingStructure.objects.create(
            type=HousingStructureTypeChoices.Semi_Intensive_Housing,
            category=HousingStructureCategoryChoices.Broilers_House,
        )
        self.flock = Flock.objects.create(
            source=flock_source,
            date_of_hatching=timezone.now() - timedelta(weeks=4),  # 4 weeks old
            chicken_type=ChickenTypeChoices.Broiler,
            initial_number_of_birds=100,
            current_rearing_method=RearingMethodChoices.Cage_System,
            current_housing_structure=broiler_house,
        )

        self.inventory = FlockInventory.objects.get(flock=self.flock)

    def test_flock_inventory_history_creation(self):
        """
        Test the creation of a flock inventory history.

        - Retrieve the flock inventory history.
        - Serialize the flock inventory history.
        - Compare the serialized data with the expected data.

        """
        inventory_history = FlockInventoryHistory.objects.get(flock_inventory=self.inventory)
        serializer = FlockInventoryHistorySerializer(instance=inventory_history)
        self.assertEqual(serializer.data['flock_inventory'], self.inventory.id)
        self.assertEqual(serializer.data['date'], self.inventory.last_update.date().strftime('%Y-%m-%d'))
        self.assertEqual(serializer.data['number_of_birds'], self.inventory.number_of_alive_birds)
        self.assertEqual(serializer.data['mortality_rate'], self.inventory.calculate_mortality_rate)
