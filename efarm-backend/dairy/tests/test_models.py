from django.db.models import QuerySet
from django.test import TestCase
from dairy.models import *


class CowTestCase(TestCase):
    def setUp(self):
        self.cow1 = Cow.objects.create(
            name="Cow1",
            breed="Friesian",
            date_of_birth=date.today() - timedelta(days=365 * 8),
            gender="Female",
            availability_status="Alive",
            pregnancy_status="Not Pregnant"
        )
        self.cow2 = Cow.objects.create(
            name="Cow2",
            breed="Jersey",
            date_of_birth=date.today() - timedelta(weeks=8),
            gender="Female",
            availability_status="Alive",
            pregnancy_status="Not Pregnant"
        )
        self.cow3 = Cow.objects.create(
            name="Cow3",
            breed="Jersey",
            date_of_birth=date.today() - timedelta(days=365 * 3),
            gender="Male",
            availability_status="Alive",
            pregnancy_status="Not Pregnant"
        )

    def test_tag_number(self):
        self.assertEqual(self.cow1.tag_number, 'FR-2015-1')

    def test_parity(self):
        self.cow2.save()
        self.assertEqual(self.cow3.parity, 0)

    def test_age(self):
        self.assertEqual(self.cow1.age, '8y, 0m')

    def test_clean(self):
        # Ensure the validation error is raised if the cow's age is greater than or equal to 7 years.
        self.cow1.date_of_birth = date.today() - timedelta(days=365 * 8)
        with self.assertRaises(ValidationError) as context:
            self.cow1.clean()
        self.assertTrue('Cow cannot be older than 7 years!' in str(context.exception))

        # Ensure the validation error is raised if the cow's status is set to "Dead" but no date of death is specified.
        self.cow3.availability_status = "Dead"
        self.cow3.date_of_death = None
        with self.assertRaises(ValidationError) as context:
            self.cow3.clean()
        self.assertTrue(
            "Sorry, this cow died! Update it's status by adding the date of death." in str(context.exception))

        # Ensure the validation error is raised if the cow's pregnancy status is set to "Pregnant" but she's less
        # than 21 months old.
        self.cow2.availability_status = "Alive"
        self.cow2.pregnancy_status = "Pregnant"
        self.cow2.date_of_birth = date.today() - timedelta(weeks=5)
        with self.assertRaises(ValidationError) as context:
            self.cow2.clean()
        self.assertTrue("Cows must be 21 months or older to be set as pregnant" in str(context.exception))


class BarnModelTestCase(TestCase):
    """
    Test case for the Barn model.

    This test case includes tests for creating and updating a Barn instance.

    """

    def test_create_barn(self):
        """
        Test creating a new Barn instance.

        It verifies that a Barn instance is created with the specified name and capacity.

        """
        barn = Barn.objects.create(name='Test Barn', capacity=10)

        self.assertEqual(barn.name, 'Test Barn')
        self.assertEqual(barn.capacity, 10)

    def test_update_barn(self):
        """
        Test updating an existing Barn instance.

        It verifies that the Barn instance is updated with the new name and capacity values.

        """
        barn = Barn.objects.create(name='Test Barn', capacity=10)
        barn.name = 'Updated Barn'
        barn.capacity = 15
        barn.save()

        updated_barn = Barn.objects.get(pk=barn.pk)

        self.assertEqual(updated_barn.name, 'Updated Barn')
        self.assertEqual(updated_barn.capacity, 15)


class CowPenModelTestCase(TestCase):
    """
    Test case for the CowPen model.

    This test case includes tests for creating a CowPen instance and changing its barn.

    """

    def setUp(self):
        """
        Set up the necessary objects for the tests.

        It creates a Barn instance and a CowPen instance.

        """
        self.barn = Barn.objects.create(name='Test Barn', capacity=10)
        self.pen = CowPen.objects.create(
            barn=self.barn,
            type=CowPenTypeChoices.Fixed,
            category=CowPenCategoriesChoices.Calf_Pen,
            capacity=5
        )

    def test_pen_creation(self):
        """
        Test creating a new CowPen instance.

        It verifies that the CowPen instance is created with the specified attributes.

        """
        self.assertEqual(self.pen.barn, self.barn)
        self.assertEqual(self.pen.type, CowPenTypeChoices.Fixed)
        self.assertEqual(self.pen.category, CowPenCategoriesChoices.Calf_Pen)
        self.assertEqual(self.pen.capacity, 5)

    def test_pen_barn_change(self):
        """
        Test changing the barn of a CowPen instance.

        It verifies that a validation error is raised when trying to change the barn of a fixed type pen.

        """
        new_barn = Barn.objects.create(name='New Barn', capacity=15)
        self.pen.barn = new_barn

        with self.assertRaises(ValidationError):
            self.pen.clean()


class CowInPenMovementModelTestCase(TestCase):
    """
    Test case for the CowInPenMovement model.

    This test case includes a test for creating a CowInPenMovement instance.

    """

    def setUp(self):
        """
        Set up the necessary objects for the test.

        It creates a Barn instance, a CowPen instance, a Cow instance, and a CowInPenMovement instance.

        """
        self.barn = Barn.objects.create(
            name='Test Barn',
            capacity=10
        )
        self.pen = CowPen.objects.create(
            barn=self.barn,
            type=CowPenTypeChoices.Movable,
            category=CowPenCategoriesChoices.Calf_Pen,
            capacity=5
        )
        self.cow = Cow.objects.create(
            name='Test Cow',
            breed=BreedChoices.Jersey,
            date_of_birth=date.today(),
            gender=SexChoices.Male,
            availability_status=CowAvailabilityChoices.Alive,
        )
        self.cow_movement: CowInPenMovement = CowInPenMovement.objects.create(
            cow=self.cow,
            previous_pen=None,
            new_pen=self.pen
        )

    def test_cow_in_pen_movement(self):
        """
        Test creating a CowInPenMovement instance.

        It verifies that the CowInPenMovement instance is created with the specified attributes.

        """
        self.assertEqual(self.cow_movement.cow, self.cow)
        self.assertIsNone(self.cow_movement.previous_pen)
        self.assertEqual(self.cow_movement.new_pen, self.pen)


class CowInBarnMovementModelTestCase(TestCase):
    """
    Test case for the CowInBarnMovement model.

    This test case includes tests for cow movements within barns and the associated barn movement signals.

    """

    def setUp(self):
        """
        Set up the necessary objects for the test.

        It creates barns, cow pens within barns, cows, and cow movements between pens.

        """
        # Create barns
        self.barn1: Barn = Barn.objects.create(name='Barn 1', capacity=10)
        self.barn2: Barn = Barn.objects.create(name='Barn 2', capacity=10)

        # Create cow pens within barns
        self.pen1_barn1: CowPen = CowPen.objects.create(
            barn=self.barn1,
            type=CowPenTypeChoices.Fixed,
            category=CowPenCategoriesChoices.General_Pen,
            capacity=5
        )
        self.pen2_barn1: CowPen = CowPen.objects.create(
            barn=self.barn1,
            type=CowPenTypeChoices.Fixed,
            category=CowPenCategoriesChoices.General_Pen,
            capacity=5
        )
        self.pen1_barn2: CowPen = CowPen.objects.create(
            barn=self.barn2,
            type=CowPenTypeChoices.Fixed,
            category=CowPenCategoriesChoices.Breeding_Pen,
            capacity=5
        )

        # Create cows
        self.cow_1: Cow = Cow.objects.create(
            name='Test Cow 1',
            breed=BreedChoices.Sahiwal,
            date_of_birth=datetime.now(),
            gender=SexChoices.Female
        )
        self.cow_2: Cow = Cow.objects.create(
            name='Test Cow 2',
            breed=BreedChoices.Sahiwal,
            date_of_birth=datetime.now(),
            gender=SexChoices.Female
        )

        # Create cow movements between pens
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

    def test_cow_in_barn_movement_signal(self):
        """
        Test the cow in barn movement signal.

        It verifies that a cow movement between pens triggers the creation of a corresponding CowInBarnMovement instance.

        """
        cow_in_barn_movement: CowInBarnMovement = CowInBarnMovement.objects.filter(cow=self.cow_2).first()
        self.assertIsNotNone(cow_in_barn_movement)
        self.assertEqual(cow_in_barn_movement.cow, self.cow_2)
        self.assertEqual(cow_in_barn_movement.previous_barn, self.pen1_barn1.barn)
        self.assertEqual(cow_in_barn_movement.new_barn, self.pen1_barn2.barn)
        self.assertIsNotNone(cow_in_barn_movement.timestamp)

    def test_cow_movement_within_pens_in_same_barn(self):
        """
        Test cow movements within pens in the same barn.

        It verifies that movements between pens within the same barn do not trigger barn movements.

        """
        barn_movements: QuerySet[CowInBarnMovement] = CowInBarnMovement.objects.filter(cow=self.cow_1)
        self.assertEqual(barn_movements.count(), 1)

    def test_cow_in_barn_movement_signal_no_previous_pen(self):
        """
        Test the cow in barn movement signal when there is no previous pen.

        It verifies that a cow movement from no previous pen to a new pen triggers the creation of a corresponding CowInBarnMovement instance.

        """
        CowInPenMovement.objects.create(
            cow=self.cow_1,
            previous_pen=None,
            new_pen=self.pen1_barn1
        )
        cow_in_barn_movement: CowInBarnMovement = CowInBarnMovement.objects.filter(cow=self.cow_1).last()

        self.assertIsNotNone(cow_in_barn_movement)
