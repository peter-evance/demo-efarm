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
        flock_source = FlockSource.objects.create(source=FlockSourceChoices.THIS_FARM)
        flock_breed = FlockBreed.objects.create(name=FlockBreedTypeChoices.KUROILER)
        broiler_house = HousingStructure.objects.create(
            type=HousingStructureTypeChoices.SEMI_INTENSIVE_HOUSING,
            category=HousingStructureCategoryChoices.BROILERS_HOUSE,
        )
        Flock.objects.create(
            source=flock_source,
            breed=flock_breed,
            date_of_hatching=timezone.now() - timedelta(weeks=4),
            chicken_type=ChickenTypeChoices.BROILER,
            initial_number_of_birds=100,
            current_rearing_method=RearingMethodChoices.CAGE_SYSTEM,
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
        flock_source = FlockSource.objects.create(source=FlockSourceChoices.THIS_FARM)
        flock_breed = FlockBreed.objects.create(name=FlockBreedTypeChoices.KUROILER)
        broiler_house = HousingStructure.objects.create(
            type=HousingStructureTypeChoices.SEMI_INTENSIVE_HOUSING,
            category=HousingStructureCategoryChoices.BROILERS_HOUSE,
        )
        self.flock = Flock.objects.create(
            source=flock_source,
            breed=flock_breed,
            date_of_hatching=timezone.now() - timedelta(weeks=4),
            chicken_type=ChickenTypeChoices.BROILER,
            initial_number_of_birds=100,
            current_rearing_method=RearingMethodChoices.CAGE_SYSTEM,
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
