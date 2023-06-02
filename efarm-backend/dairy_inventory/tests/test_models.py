from django.db.models import QuerySet
from django.test import TestCase

from dairy_inventory.models import *


class CowInventoryTestCase(TestCase):
    """
    Test case for the CowInventory model.

    Tests the functionality of the cow inventory signal and the associated models.

    """

    def setUp(self):
        """
        Set up the test case by creating cows with different availability statuses.

        """

        self.cow_1: Cow = Cow.objects.create(
            name='Daisy',
            breed=BreedChoices.Friesian,
            date_of_birth=date.today() - timedelta(days=1460),
            gender=SexChoices.Female,
            pregnancy_status=PregnancyChoices.Open
        )
        self.cow_2: Cow = Cow.objects.create(
            name='Bella',
            breed=BreedChoices.Jersey,
            date_of_birth=date.today() - timedelta(days=1000),
            gender=SexChoices.Male,
            pregnancy_status=PregnancyChoices.Open
        )
        self.cow_3: Cow = Cow.objects.create(
            name='Biggie',
            breed=BreedChoices.Friesian,
            date_of_birth=date.today() - timedelta(days=1460),
            gender=SexChoices.Male,
            availability_status=CowAvailabilityChoices.Dead,
            pregnancy_status=PregnancyChoices.Open
        )
        self.cow_4: Cow = Cow.objects.create(
            name='Christine',
            breed=BreedChoices.Jersey,
            date_of_birth=date.today() - timedelta(days=1000),
            gender=SexChoices.Female,
            availability_status=CowAvailabilityChoices.Sold,
            pregnancy_status=PregnancyChoices.Open
        )

    def test_update_cow_inventory(self):
        """
        Test the functionality of the cow inventory signal and history creation.

        - Ensure the cow inventory signal updates the CowInventory model correctly.
        - Ensure a new history entry is created.

        """

        cow_inventory: CowInventory = CowInventory.objects.first()
        self.assertIsNotNone(cow_inventory)
        self.assertEqual(cow_inventory.total_number_of_cows, 2)
        self.assertEqual(cow_inventory.number_of_male_cows, 1)
        self.assertEqual(cow_inventory.number_of_female_cows, 1)
        self.assertEqual(cow_inventory.number_of_sold_cows, 1)
        self.assertEqual(cow_inventory.number_of_dead_cows, 1)

        history_entries: QuerySet[CowInventoryUpdateHistory] = CowInventoryUpdateHistory.objects.all()
        self.assertIsNotNone(history_entries)
        self.assertEqual(history_entries.count(), 4)


class BarnInventoryTestCase(TestCase):
    """
    Test case for the BarnInventory model.

    Tests the functionality of adding and removing cows from barn inventories.

    """

    def setUp(self):
        """
        Set up the test case by creating barns, pens, cows, and cow pen movements.

        """

        self.barn1: Barn = Barn.objects.create(name='Test Barn', capacity=10)
        self.barn2: Barn = Barn.objects.create(name='Test Barn', capacity=10)
        self.pen1_barn1: CowPen = CowPen.objects.create(
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
        self.cow1: Cow = Cow.objects.create(
            name='Test Cow',
            breed=BreedChoices.Jersey,
            date_of_birth=date.today(),
            gender=SexChoices.Female,
            availability_status=CowAvailabilityChoices.Alive,
        )
        self.cow2: Cow = Cow.objects.create(
            name='Test Cow',
            breed=BreedChoices.Jersey,
            date_of_birth=date.today(),
            gender=SexChoices.Male,
            availability_status=CowAvailabilityChoices.Alive,
        )
        self.cow_in_pen_movement: CowInPenMovement = CowInPenMovement.objects.create(
            cow=self.cow1,
            previous_pen=None,
            new_pen=self.pen1_barn1
        )
        self.inventory_1: BarnInventory = BarnInventory.objects.get(barn=self.barn1)
        self.inventory_2: BarnInventory = BarnInventory.objects.get(barn=self.barn2)

    def test_add_cow_method_called(self):
        """
        Test the behavior of adding a cow to the barn inventory.

        - Assert that the number of cows in the inventory has increased.

        """

        self.assertEqual(self.inventory_1.number_of_cows, 1)

    def test_add_cow_method_behavior_at_capacity(self):
        """
        Test the behavior of adding a cow to a full barn inventory.

        - Fill up the barn to capacity.
        - Attempt to add a cow to the inventory (should raise an error).
        - Assert that the number of cows in the inventory remains at capacity.

        """

        self.inventory_1.number_of_cows = self.inventory_1.barn.capacity
        self.inventory_1.save()

        with self.assertRaises(ValueError):
            self.inventory_1.add_cow()

        self.assertEqual(self.inventory_1.number_of_cows, self.inventory_1.barn.capacity)

    def test_remove_cow_method_called(self):
        """
        Test the behavior of removing a cow from the barn inventory.

        - Create a cow pen movement that moves the cow out of the barn.
        - Refresh the inventory from the database.
        - Assert that the number of cows in the inventory has decreased.

        """

        CowInPenMovement.objects.create(
            cow=self.cow1,
            previous_pen=self.pen1_barn1,
            new_pen=self.pen1_barn2
        )
        self.inventory_1.refresh_from_db()

        self.assertEqual(self.inventory_1.number_of_cows, 0)

    def test_remove_cow_empty_inventory(self):
        """
        Test the behavior of removing a cow from an empty barn inventory.

        - Remove a cow from an empty inventory (should not decrease the count).
        - Assert that the number of cows in the inventory remains at 0.

        """

        CowInPenMovement.objects.create(
            cow=self.cow2,
            previous_pen=self.pen1_barn2,
            new_pen=self.pen1_barn1
        )

        self.assertEqual(self.inventory_2.number_of_cows, 0)


class BarnInventoryHistoryTestCase(TestCase):
    """
    Test case for the BarnInventoryHistory model.

    Tests the functionality of creating barn inventory history entries.

    """

    def setUp(self):
        """
        Set up the test case by creating barns, cow pens, cows, and cow pen movements.

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

    def test_create_barn_inventory_history(self):
        """
        Test the functionality of creating barn inventory history entries.

        - Create a cow pen movement.
        - Refresh the barn inventories.
        - Assert that a barn inventory history entry is created with the correct details.

        """

        CowInPenMovement.objects.create(
            cow=self.cow,
            previous_pen=self.pen1_barn,
            new_pen=self.pen1_barn2
        )
        BarnInventory.objects.get(barn=self.barn1).refresh_from_db()
        BarnInventory.objects.get(barn=self.barn1).refresh_from_db()

        inventory: BarnInventory = BarnInventory.objects.get(barn=self.barn2)

        # Assert that the barn inventory history is created
        self.assertEqual(BarnInventoryHistory.objects.count(), 2)
        latest_history: BarnInventoryHistory = BarnInventoryHistory.objects.latest('timestamp')
        self.assertEqual(latest_history.barn_inventory, inventory)
        self.assertEqual(latest_history.number_of_cows, inventory.number_of_cows)

    def test_create_barn_inventory_history_on_remove_cow(self):
        """
        Test the functionality of creating barn inventory history entries after removing a cow.

        - Create cow pen movements.
        - Retrieve the barn inventory.
        - Assert that a barn inventory history entry is created with the correct details.

        """

        CowInPenMovement.objects.create(
            cow=self.cow,
            previous_pen=None,
            new_pen=self.pen1_barn
        )
        CowInPenMovement.objects.create(
            cow=self.cow,
            previous_pen=self.pen1_barn,
            new_pen=self.pen1_barn2
        )
        inventory: BarnInventory = BarnInventory.objects.get(barn=self.barn2)

        # Assert that the barn inventory history is created after removing a cow
        self.assertEqual(BarnInventoryHistory.objects.count(), 3)
        latest_history: BarnInventoryHistory = BarnInventoryHistory.objects.latest('timestamp')
        self.assertEqual(latest_history.barn_inventory, inventory)
        self.assertEqual(latest_history.number_of_cows, inventory.number_of_cows)


class CowPenInventoryTestCase(TestCase):
    """
    Test case for the CowPenInventory model.

    Tests the functionality of adding and removing cows from cow pen inventories.

    """

    def setUp(self):
        """
        Set up the test case by creating a barn, cow pens, and cows.

        """

        self.barn: Barn = Barn.objects.create(name='Test Barn', capacity=10)
        self.pen_1: CowPen = CowPen.objects.create(
            barn=self.barn,
            type=CowPenTypeChoices.Fixed,
            category=CowPenCategoriesChoices.Heifer_Pen,
            capacity=2
        )
        self.pen_2: CowPen = CowPen.objects.create(
            barn=self.barn,
            type=CowPenTypeChoices.Fixed,
            category=CowPenCategoriesChoices.General_Pen,
            capacity=5
        )
        # Create cows
        self.cow_1: Cow = Cow.objects.create(
            name='Daisy',
            breed=BreedChoices.Friesian,
            date_of_birth=date.today() - timedelta(days=1460),
            gender=SexChoices.Female,
            pregnancy_status=PregnancyChoices.Open
        )
        self.cow_2: Cow = Cow.objects.create(
            name='Bella',
            breed=BreedChoices.Jersey,
            date_of_birth=date.today() - timedelta(days=1000),
            gender=SexChoices.Female,
            pregnancy_status=PregnancyChoices.Open
        )
        self.cow_in_pen_movement_1: CowInPenMovement = CowInPenMovement.objects.create(
            cow=self.cow_1,
            previous_pen=None,
            new_pen=self.pen_1
        )

    def test_create_pen_creates_inventory(self):
        """
        Test the creation of cow pen inventories.

        - Check if a corresponding cow pen inventory is created.
        - Assert that a single cow pen inventory is created for the cow pen.

        """

        # Check if a corresponding cow pen inventory is created
        self.assertTrue(CowPenInventory.objects.filter(pen=self.pen_1).exists())
        self.assertEqual(CowPenInventory.objects.filter(pen=self.pen_1).count(), 1)

    def test_add_cow_method(self):
        """
        Test the functionality of adding a cow to a cow pen inventory.

        - Add a cow to the pen inventory.
        - Refresh the pen inventory from the database.
        - Assert that the number of cows in the pen has increased.

        """

        pen_inventory: CowPenInventory = CowPenInventory.objects.get(pen=self.pen_1)
        pen_inventory.add_cow()  # Created this shortcut instead of creating a whole new cow in pen movement
        # serves the same purpose as creating a new movement triggers a signal which invokes this method

        pen_inventory.refresh_from_db()

        # Retrieve the updated cow pen inventory from the database
        updated_pen_inventory: CowPenInventory = CowPenInventory.objects.get(pk=pen_inventory.pk)

        # Assert that the number of cows in the pen has increased
        self.assertEqual(updated_pen_inventory.number_of_cows, 2)

    def test_remove_cow_method(self):
        """
        Test the functionality of removing a cow from a cow pen inventory.

        - Remove a cow from the pen inventory.
        - Refresh the pen inventory from the database.
        - Assert that the number of cows in the pen has decreased.

        """

        pen_inventory: CowPenInventory = CowPenInventory.objects.get(pen=self.pen_1)
        # Remove a cow from the pen
        pen_inventory.remove_cow()

        pen_inventory.refresh_from_db()

        # Retrieve the updated cow pen inventory from the database
        updated_pen_inventory: CowPenInventory = CowPenInventory.objects.get(pk=pen_inventory.pk)

        # Assert that the number of cows in the pen has decreased
        self.assertEqual(updated_pen_inventory.number_of_cows, 0)

    def test_add_cow_exceed_capacity(self):
        """
        Test adding a cow to a cow pen inventory when the capacity is exceeded.

        - Add a cow to the pen inventory.
        - Try to add another cow to the pen, which should raise a ValueError.
        - Retrieve the cow pen inventory from the database.
        - Assert that the number of cows in the pen remains the same.

        """

        pen_inventory: CowPenInventory = CowPenInventory.objects.get(pen=self.pen_1)
        pen_inventory.add_cow()  # Same as above explainer for the method (`add_cow`)

        # Try to add another cow to the pen, which should raise a ValueError
        with self.assertRaises(ValueError):
            pen_inventory.add_cow()  # Same as above explainer for the method (`add_cow`)

        # Retrieve the cow pen inventory from the database
        updated_pen_inventory: CowPenInventory = CowPenInventory.objects.get(pk=pen_inventory.pk)

        # Assert that the number of cows in the pen remains the same
        self.assertEqual(updated_pen_inventory.number_of_cows, 2)

    def test_update_pen_inventory_signal(self):
        """
        Test the functionality of the update pen inventory signal.

        - Create cow pen movements.
        - Check if the cow pen inventories are updated correctly.
        - Assert that the number of cows is updated in the inventories.

        """

        # Create a cow in pen movement to cow pen 2
        CowInPenMovement.objects.create(
            cow=self.cow_2,
            previous_pen=None,
            new_pen=self.pen_2
        )

        # Check if the cow pen inventories are updated correctly
        pen_inventory_1: CowPenInventory = CowPenInventory.objects.get(pen=self.pen_1)
        pen_inventory_2: CowPenInventory = CowPenInventory.objects.get(pen=self.pen_2)

        # Assert that the number of cows is updated in the inventories
        self.assertEqual(pen_inventory_1.number_of_cows, 1)
        self.assertEqual(pen_inventory_2.number_of_cows, 1)

        # Create a cow in pen movement from cow pen 2 to cow pen 1
        CowInPenMovement.objects.create(
            cow=self.cow_2,
            previous_pen=self.pen_2,
            new_pen=self.pen_1
        )

        # Check if the cow pen inventories are updated correctly after the removal
        pen_inventory_1.refresh_from_db()
        pen_inventory_2.refresh_from_db()

        # Assert that the number of cows is updated in the inventories
        self.assertEqual(pen_inventory_1.number_of_cows, 2)
        self.assertEqual(pen_inventory_2.number_of_cows, 0)


class CowPenHistoryTestCase(TestCase):
    def setUp(self):
        """
        Set up the test case by creating a barn, cow pen, and cow pen inventory.

        """

        self.barn: Barn = Barn.objects.create(name='Test Barn', capacity=10)
        self.pen: CowPen = CowPen.objects.create(
            barn=self.barn,
            type=CowPenTypeChoices.Movable,
            category=CowPenCategoriesChoices.Breeding_Pen,
            capacity=2
        )

    def test_create_pen_history_signal(self):
        """
        Test the functionality of the creation pen history signal.

        - Retrieve the created cow pen history entries.
        - Assert that a new history entry is created.
        - Retrieve the created history entry.
        - Assert that the history entry has the correct attributes.

        """

        pen_inventory: CowPenInventory = CowPenInventory.objects.get(pen=self.pen)

        # Retrieve the created cow pen history entries
        history_entries: QuerySet[CowPenHistory] = CowPenHistory.objects.filter(pen=self.pen)

        # Assert that a new history entry is created
        self.assertEqual(history_entries.count(), 1)

        # Retrieve the created history entry
        history_entry: CowPenHistory = history_entries.first()

        # Assert that the history entry has the correct attributes
        self.assertEqual(history_entry.pen, self.pen)
        self.assertEqual(history_entry.barn, self.barn)
        self.assertEqual(history_entry.type, self.pen.type)
        self.assertEqual(history_entry.number_of_cows, pen_inventory.number_of_cows)
        self.assertIsNotNone(history_entry.timestamp)


class CowInventoryUpdateHistoryTestCase(TestCase):
    def setUp(self):
        """
        Set up the test case by creating a cow and retrieving the history entries after the CowInventory instance is created.

        """

        self.cow: Cow = Cow.objects.create(
            name='Daisy',
            breed=BreedChoices.Friesian,
            date_of_birth=date.today() - timedelta(days=1460),
            gender=SexChoices.Female,
            pregnancy_status=PregnancyChoices.Open
        )

        # Retrieve the history entries after the CowInventory instance is created
        self.history_entries = CowInventoryUpdateHistory.objects.all()

    def test_create_cow_inventory_update_history_signal(self):
        """
        Test the functionality of the creation cow inventory update history signal.

        - Ensure that the history entry is created.

        """

        # Ensure that the history entry is created
        self.assertEqual(self.history_entries.count(), 1)


class MilkInventoryModelTestCase(TestCase):
    def setUp(self):
        self.cow = Cow.objects.create(
            name='Daisy',
            breed=BreedChoices.Friesian,
            date_of_birth=date.today() - timedelta(days=1460),
            gender=SexChoices.Female,
            pregnancy_status=PregnancyChoices.Open)
        self.pregnancy = Pregnancy.objects.create(
            cow=self.cow,
            start_date=date.today() - timedelta(days=300),
            date_of_calving=date.today() - timedelta(days=15),
            pregnancy_status='Confirmed',
            pregnancy_outcome='Live')
        self.milk_record = Milk.objects.create(
            cow=self.cow,
            amount_in_kgs=20.5,
            lactation=self.cow.lactation_set.last())

    def test_milk_inventory_creation(self):
        milk_inventory = MilkInventory.objects.get(id=1)
        self.assertEqual(milk_inventory.total_amount_in_kgs, 20.5)

    def test_milk_inventory_update_history_creation(self):
        milk_inventory = MilkInventory.objects.get(id=1)
        self.assertEqual(milk_inventory.total_amount_in_kgs, 20.5)
        milk_update_history: MilkInventoryUpdateHistory = MilkInventoryUpdateHistory.objects.get(id=1)
        self.assertEqual(milk_update_history.amount_in_kgs, 20.5)

