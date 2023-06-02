from django.test import TestCase

from dairy.serializers import *


class CowPenSerializerTestCase(TestCase):
    """
    Test case for the CowPenSerializer.

    This test case validates the serialization of a CowPen instance.

    """

    def setUp(self):
        """
        Set up the necessary objects for the test.

        It creates a Barn object and a CowPen object.

        """
        self.barn: Barn = Barn.objects.create(name='Test Barn', capacity=10)
        self.pen: CowPen = CowPen.objects.create(
            barn=self.barn,
            type=CowPenTypeChoices.Fixed,
            category=CowPenCategoriesChoices.Calf_Pen,
            capacity=5
        )

    def test_pen_serializer(self):
        """
        Test the serialization of a CowPen instance.

        It verifies that the serialized data matches the expected data.

        """
        serializer: CowPenSerializer = CowPenSerializer(instance=self.pen)
        serialized_data = serializer.data

        expected_data = {
            'id': self.pen.id,
            'barn': self.barn.id,
            'type': CowPenTypeChoices.Fixed,
            'category': CowPenCategoriesChoices.Calf_Pen,
            'capacity': 5
        }

        self.assertDictEqual(serialized_data, expected_data)


class BarnSerializerTestCase(TestCase):
    """
    Test case for the BarnSerializer.

    This test case validates the serialization of a Barn instance.

    """

    def setUp(self):
        """
        Set up the necessary objects for the test.

        It creates a Barn object.

        """
        self.barn: Barn = Barn.objects.create(name='Test Barn', capacity=10)

    def test_serialize_barn(self):
        """
        Test the serialization of a Barn instance.

        It verifies that the serialized data matches the expected data.

        """
        serializer: BarnSerializer = BarnSerializer(instance=self.barn)
        serialized_data = serializer.data

        expected_data = {
            'id': self.barn.id,
            'name': 'Test Barn',
            'capacity': 10
        }

        self.assertDictEqual(serialized_data, expected_data)


class CowInPenMovementSerializerTestCase(TestCase):
    """
    Test case for the CowInPenMovementSerializer.

    This test case validates the serialization of a CowInPenMovement instance.

    """

    def setUp(self):
        """
        Set up the necessary objects for the test.

        It creates a Barn object, two CowPen objects, a Cow object,
        and two CowInPenMovement objects.

        """
        self.barn: Barn = Barn.objects.create(name='Test Barn', capacity=10)
        self.pen_1: CowPen = CowPen.objects.create(
            barn=self.barn,
            type=CowPenTypeChoices.Fixed,
            category=CowPenCategoriesChoices.Calf_Pen,
            capacity=5
        )
        self.pen_2: CowPen = CowPen.objects.create(
            barn=self.barn,
            type=CowPenTypeChoices.Movable,
            category=CowPenCategoriesChoices.Heifer_Pen,
            capacity=5
        )
        self.cow: Cow = Cow.objects.create(
            name='Daisy',
            breed=BreedChoices.Friesian,
            date_of_birth=date.today() - timedelta(days=1460),
            gender=SexChoices.Female,
            pregnancy_status=PregnancyChoices.Open
        )
        self.cow_in_pen_movement_1: CowInPenMovement = CowInPenMovement.objects.create(
            cow=self.cow,
            previous_pen=self.pen_1,
            new_pen=self.pen_2
        )
        self.cow_in_pen_movement_2: CowInPenMovement = CowInPenMovement.objects.create(
            cow=self.cow,
            previous_pen=None,
            new_pen=self.pen_2
        )

    def test_cow_in_pen_movement_serializer(self):
        """
        Test the serialization of a CowInPenMovement instance.

        It verifies that the serialized data matches the expected data.

        """
        serializer: CowInPenMovementSerializer = CowInPenMovementSerializer(instance=self.cow_in_pen_movement_1)
        serialized_data = serializer.data

        expected_data = {
            'id': self.cow_in_pen_movement_1.id,
            'cow': self.cow.pk,
            'previous_pen': self.pen_1.pk,
            'new_pen': self.pen_2.pk,
            'timestamp': self.cow_in_pen_movement_1.timestamp.astimezone().isoformat(),
        }

        self.assertDictEqual(serialized_data, expected_data)

    def test_cow_in_pen_movement_serializer_no_previous_pen(self):
        """
        Test the serialization of a CowInPenMovement instance with no previous pen.

        It verifies that the serialized data matches the expected data when there is no previous pen.

        """
        serializer = CowInPenMovementSerializer(instance=self.cow_in_pen_movement_2)
        serialized_data = serializer.data

        expected_data = {
            'id': self.cow_in_pen_movement_2.id,
            'cow': self.cow.pk,
            'previous_pen': None,
            'new_pen': self.pen_2.pk,
            'timestamp': self.cow_in_pen_movement_2.timestamp.astimezone().isoformat(),
        }

        self.assertDictEqual(serialized_data, expected_data)


class CowInBarnMovementSerializerTestCase(TestCase):
    """
    Test case for the CowInBarnMovementSerializer.

    This test case validates the serialization of a CowInBarnMovement instance.

    """

    def setUp(self):
        """
        Set up the necessary objects for the test.

        It creates barns, cow pens, cows, and cow movements.

        """
        self.barn1: Barn = Barn.objects.create(name='Barn 1', capacity=10)
        self.barn2: Barn = Barn.objects.create(name='Barn 2', capacity=15)
        self.pen1_barn1: CowPen = CowPen.objects.create(
            barn=self.barn1,
            type=CowPenTypeChoices.Movable,
            category=CowPenCategoriesChoices.Sick_Pen,
            capacity=5
        )
        self.pen2_barn1: CowPen = CowPen.objects.create(
            barn=self.barn1,
            type=CowPenTypeChoices.Fixed,
            category=CowPenCategoriesChoices.Heifer_Pen,
            capacity=3
        )
        self.pen1_barn2: CowPen = CowPen.objects.create(
            barn=self.barn2,
            type=CowPenTypeChoices.Fixed,
            category=CowPenCategoriesChoices.Sick_Pen,
            capacity=9
        )

        self.cow_1: Cow = Cow.objects.create(
            name='Test Cow 1',
            breed=BreedChoices.Crossbreed,
            date_of_birth=date.today(),
            gender=SexChoices.Male,
            availability_status=CowAvailabilityChoices.Alive,
        )
        self.cow_2: Cow = Cow.objects.create(
            name='Test Cow 2',
            breed=BreedChoices.Ayrshire,
            date_of_birth=date.today(),
            gender=SexChoices.Female,
            availability_status=CowAvailabilityChoices.Alive,
        )
        self.cow_in_pen_movement_1: CowInPenMovement = CowInPenMovement.objects.create(
            cow=self.cow_1,
            previous_pen=self.pen1_barn1,
            new_pen=self.pen2_barn1
        )
        self.cow_in_pen_movement_2: CowInPenMovement = CowInPenMovement.objects.create(
            cow=self.cow_2,
            previous_pen=self.pen1_barn1,
            new_pen=self.pen1_barn2
        )

    def test_cow_in_barn_movement_serializer(self):
        """
        Test the serialization of a CowInBarnMovement instance.

        It verifies that the serialized data matches the expected data.

        """
        cow_in_barn_movement: CowInBarnMovement = CowInBarnMovement.objects.filter(cow=self.cow_2).first()
        serializer: CowInBarnMovementSerializer = CowInBarnMovementSerializer(cow_in_barn_movement)
        serialized_data = serializer.data

        expected_data = {
            'id': cow_in_barn_movement.id,
            'cow': self.cow_2.id,
            'previous_barn': self.pen1_barn1.barn.id,
            'new_barn': self.pen1_barn2.barn.id,
            'timestamp': cow_in_barn_movement.timestamp.astimezone().isoformat()
        }

        self.assertDictEqual(serialized_data, expected_data)

    def test_cow_in_barn_movement_serializer_no_previous_pen(self):
        """
        Test the serialization of a CowInBarnMovement instance with no previous pen.

        It creates a new cow and cow movement with no previous pen,
        and verifies that the serialized data matches the expected data.

        """
        cow: Cow = Cow.objects.create(
            name='Test Cow 3',
            breed=BreedChoices.Jersey,
            date_of_birth=date.today(),
            gender=SexChoices.Male,
            availability_status=CowAvailabilityChoices.Alive,
        )
        CowInPenMovement.objects.create(
            cow=cow,
            previous_pen=None,
            new_pen=self.pen1_barn1
        )
        cow_in_barn_movement: CowInBarnMovement = CowInBarnMovement.objects.filter(cow=cow).first()
        serializer: CowInBarnMovementSerializer = CowInBarnMovementSerializer(cow_in_barn_movement)

        expected_data = {
            'id': cow_in_barn_movement.id,
            'cow': cow.pk,
            'previous_barn': None,
            'new_barn': self.pen1_barn1.pk,
            'timestamp': cow_in_barn_movement.timestamp.astimezone().isoformat()
        }

        self.assertDictEqual(serializer.data, expected_data)
