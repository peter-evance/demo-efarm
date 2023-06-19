from django.test import TestCase
from datetime import date, timedelta
from poultry.models import *
from poultry.choices import *
from poultry_inventory.models import *


class FlockInventoryTestCase(TestCase):
    """
    Test case for the FlockInventory model.

    This test case verifies the creation of flock inventories and their history.

    """

    def setUp(self):
        """
        Set up the test case by creating a flock, flock source, and a housing structure.

        """
        flock_source: FlockSource = FlockSource.objects.create(source=FlockSourceChoices.THIS_FARM)
        flock_breed = FlockBreed.objects.create(name=FlockBreedTypeChoices.KUROILER)

        broiler_house: HousingStructure = HousingStructure.objects.create(
            type=HousingStructureTypeChoices.SEMI_INTENSIVE_HOUSING,
            category=HousingStructureCategoryChoices.BROILERS_HOUSE,
        )

        Flock.objects.create(
            source=flock_source,
            breed=flock_breed,
            date_of_hatching=date.today() - timedelta(weeks=4),  # 4 weeks old
            chicken_type=ChickenTypeChoices.BROILER,
            initial_number_of_birds=100,
            current_rearing_method=RearingMethodChoices.CAGE_SYSTEM,
            current_housing_structure=broiler_house,
        )

    def test_flock_inventory_creation(self):
        """
        Test the creation of a flock inventory.

        - Retrieve the first flock and inventory objects.
        - Assert that the inventory is associated with the flock.
        - Assert that the number of alive birds in the inventory matches the initial number of birds of the flock.
        - Assert that the number of dead birds in the inventory is 0.

        """
        flock: Flock = Flock.objects.first()
        inventory: FlockInventory = FlockInventory.objects.first()

        self.assertEqual(inventory.flock, flock)
        self.assertEqual(inventory.number_of_alive_birds, flock.initial_number_of_birds)
        self.assertEqual(inventory.number_of_dead_birds, 0)

    def test_flock_inventory_history_creation(self):
        """
        Test the creation of a flock inventory history.

        - Retrieve the first inventory and history objects.
        - Assert that the history is associated with the inventory.
        - Assert that the date of the history matches the last update date of the inventory.
        - Assert that the number of birds in the history matches the number of alive birds in the inventory.
        - Assert that the mortality rate in the history matches the calculated mortality rate of the inventory.

        """
        inventory: FlockInventory = FlockInventory.objects.first()
        history: FlockInventoryHistory = FlockInventoryHistory.objects.first()

        self.assertEqual(history.flock_inventory, inventory)
        self.assertEqual(history.date, inventory.last_update.date())
        self.assertEqual(history.number_of_birds, inventory.number_of_alive_birds)
        self.assertEqual(history.mortality_rate, inventory.calculate_mortality_rate)


class FlockMovementTestCase(TestCase):
    """
    Test case for the FlockMovement model.

    This test case verifies the creation of flock movements.

    """

    def setUp(self):
        """
        Set up the test case by creating a flock, flock source, and housing structures.

        """
        flock_source: FlockSource = FlockSource.objects.create(source=FlockSourceChoices.THIS_FARM)
        flock_breed = FlockBreed.objects.create(name=FlockBreedTypeChoices.KUROILER)

        self.from_structure: HousingStructure = HousingStructure.objects.create(
            type=HousingStructureTypeChoices.CLOSED_SHED,
            category=HousingStructureCategoryChoices.BROILERS_HOUSE,
        )
        self.to_structure: HousingStructure = HousingStructure.objects.create(
            type=HousingStructureTypeChoices.SEMI_INTENSIVE_HOUSING,
            category=HousingStructureCategoryChoices.BROILERS_HOUSE,
        )

        self.flock: Flock = Flock.objects.create(
            source=flock_source,
            breed=flock_breed,
            date_of_hatching=date.today() - timedelta(weeks=4),  # 4 weeks old
            chicken_type=ChickenTypeChoices.BROILER,
            initial_number_of_birds=100,
            current_rearing_method=RearingMethodChoices.CAGE_SYSTEM,
            current_housing_structure=self.from_structure,
        )

    def test_valid_flock_movement(self):
        """
        Test the creation of a valid flock movement.

        - Create a flock movement with the given flock, from_structure, and to_structure.
        - Assert that the flock in the movement matches the original flock.
        - Assert that the from_structure in the movement matches the original from_structure.
        - Assert that the to_structure in the movement matches the original to_structure.

        """
        movement: FlockMovement = FlockMovement.objects.create(
            flock=self.flock,
            from_structure=self.from_structure,
            to_structure=self.to_structure
        )

        self.assertEqual(movement.flock, self.flock)
        self.assertEqual(movement.from_structure, self.from_structure)
        self.assertEqual(movement.to_structure, self.to_structure)
