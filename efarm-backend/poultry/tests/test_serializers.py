from django.test import TestCase

from poultry.choices import *
from poultry.models import *
from poultry.serializers import *


class FlockSourceSerializerTestCase(TestCase):
    """
    Test case for the FlockSourceSerializer.
    """

    def setUp(self):
        """
        Set up the test case by creating a flock source.
        """
        self.flock_source: FlockSource = FlockSource.objects.create(source=FlockSourceChoices.This_Farm)

    def test_serialize_flock_source(self):
        """
        Test the serialization of a flock source.

        Asserts that the serialized data matches the expected data.
        """
        serializer: FlockSourceSerializer = FlockSourceSerializer(instance=self.flock_source)
        serialized_data: dict = serializer.data

        expected_data: dict = {
            'id': self.flock_source.id,
            'source': 'This Farm'
        }

        self.assertDictEqual(serialized_data, expected_data)


class HousingStructureSerializerTestCase(TestCase):
    """
    Test case for the HousingStructureSerializer.
    """

    def setUp(self):
        """
        Set up the test case by creating a housing structure.
        """
        self.housing_structure: HousingStructure = HousingStructure.objects.create(
            type=HousingStructureTypeChoices.Deep_Litter_House,
            category=HousingStructureCategoryChoices.Breeders_House
        )

    def test_serialize_housing_structure(self):
        """
        Test the serialization of a housing structure.

        Asserts that the serialized data matches the expected data.
        """
        serializer: HousingStructureSerializer = HousingStructureSerializer(instance=self.housing_structure)
        serialized_data: dict = serializer.data

        expected_data: dict = {
            'id': self.housing_structure.id,
            'type': 'Deep Litter House',
            'category': 'Breeders House'
        }

        self.assertDictEqual(serialized_data, expected_data)


class FlockSerializerTestCase(TestCase):
    """
    Test case for the FlockSerializer.
    """

    def setUp(self):
        """
        Set up the test case by creating a flock, flock source, and housing structure.
        """
        self.flock_source: FlockSource = FlockSource.objects.create(source=FlockSourceChoices.Kiplels_Farm)
        self.housing_structure: HousingStructure = HousingStructure.objects.create(
            type=HousingStructureTypeChoices.Deep_Litter_House,
            category=HousingStructureCategoryChoices.Growers_House
        )
        self.flock: Flock = Flock.objects.create(
            source=self.flock_source,
            date_of_hatching=date.today() - timedelta(weeks=9),
            chicken_type=ChickenTypeChoices.Layers,
            initial_number_of_birds=10,
            current_rearing_method=RearingMethodChoices.Deep_Litter,
            current_housing_structure=self.housing_structure
        )

    def test_serialize_flock(self):
        """
        Test the serialization of a flock.

        Asserts that the serialized data matches the expected data.
        """
        serializer: FlockSerializer = FlockSerializer(instance=self.flock)
        serialized_data: dict = serializer.data

        expected_data: dict = {
            'id': self.flock.id,
            'source': self.flock_source.id,
            'date_of_hatching': str(self.flock.date_of_hatching),
            'chicken_type': ChickenTypeChoices.Layers,
            'initial_number_of_birds': 10,
            'current_rearing_method': RearingMethodChoices.Deep_Litter,
            'current_housing_structure': self.housing_structure.id,
            'date_established': str(self.flock.date_established),
            'age_in_weeks': 9,
            'age_in_months': 2,
            'age_in_weeks_in_farm': 0,
            'age_in_months_in_farm': 0,
        }

        self.assertDictEqual(serialized_data, expected_data)


class FlockHistorySerializerTestCase(TestCase):
    """
    Test case for the FlockHistorySerializer.
    """

    def setUp(self):
        """
        Set up the test case by creating a flock, flock source, housing structure, and flock history.
        """
        self.housing_structure: HousingStructure = HousingStructure.objects.create(
            type=HousingStructureTypeChoices.Deep_Litter_House,
            category=HousingStructureCategoryChoices.Growers_House
        )
        self.flock: Flock = Flock.objects.create(
            source=FlockSource.objects.create(source=FlockSourceChoices.Kiplels_Farm),
            date_of_hatching=date.today() - timedelta(weeks=9),
            chicken_type=ChickenTypeChoices.Layers,
            initial_number_of_birds=10,
            current_rearing_method=RearingMethodChoices.Deep_Litter,
            current_housing_structure=self.housing_structure,
        )
        self.flock_history: FlockHistory = FlockHistory.objects.get(flock=self.flock)

    def test_serialize_flock_history(self):
        """
        Test the serialization of a flock history.

        Asserts that the serialized data matches the expected data.
        """
        serializer: FlockHistorySerializer = FlockHistorySerializer(instance=self.flock_history)
        serialized_data: dict = serializer.data

        expected_data: dict = {
            'id': self.flock_history.id,
            'flock': self.flock.id,
            'rearing_method': RearingMethodChoices.Deep_Litter,
            'current_housing_structure': self.housing_structure.id,
            'date_changed': self.flock_history.date_changed.astimezone().isoformat(),
        }
        self.assertDictEqual(serialized_data, expected_data)


class FlockMovementSerializerTestCase(TestCase):
    """
    Test case for the FlockMovementSerializer.

    This test case verifies the serialization and deserialization of flock movements.

    """

    def setUp(self):
        """
        Set up the test case by creating housing structures, a flock, and flock movement data.

        """
        self.from_structure = HousingStructure.objects.create(
            type=HousingStructureTypeChoices.Deep_Litter_House,
            category=HousingStructureCategoryChoices.Growers_House
        )
        self.to_structure = HousingStructure.objects.create(
            type=HousingStructureTypeChoices.Deep_Litter_House,
            category=HousingStructureCategoryChoices.Growers_House
        )
        self.flock_source: FlockSource = FlockSource.objects.create(source=FlockSourceChoices.Kiplels_Farm)
        self.flock = Flock.objects.create(
            source=self.flock_source,
            date_of_hatching=date.today() - timedelta(weeks=9),
            chicken_type=ChickenTypeChoices.Layers,
            initial_number_of_birds=100,
            current_rearing_method=RearingMethodChoices.Cage_System,
            current_housing_structure=self.from_structure,
        )

        self.flock_movement_data = {
            'flock': self.flock.id,
            'from_structure': self.from_structure.id,
            'to_structure': self.to_structure.id
        }

    def test_flock_movement_serializer(self):
        """
        Test the serialization of flock movement data.

        - Create a flock movement serializer with valid data.
        - Validate the serializer.
        - Save the serializer data and retrieve the flock movement object.
        - Compare the saved data with the expected data.

        """
        serializer = FlockMovementSerializer(data=self.flock_movement_data)
        self.assertTrue(serializer.is_valid())

        flock_movement = serializer.save()
        self.assertEqual(flock_movement.flock.id, self.flock_movement_data['flock'])
        self.assertEqual(flock_movement.from_structure.id, self.flock_movement_data['from_structure'])
        self.assertEqual(flock_movement.to_structure.id, self.flock_movement_data['to_structure'])

        # Additional assertions to test other fields if needed
        self.assertEqual(
            str(flock_movement),
            f'Movement of Flock {flock_movement.flock_id} ({self.from_structure} -> {self.to_structure})'
        )

    def test_flock_movement_serializer_invalid_data(self):
        """
        Test the serialization of flock movement data with invalid data.

        - Create a flock movement serializer with invalid data.
        - Validate the serializer and check for errors.

        """
        invalid_data = {
            'flock': 1,
            'from_structure': self.from_structure.id,
            'to_structure': 999999,  # An Invalid housing structure ID
        }

        serializer = FlockMovementSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('to_structure', serializer.errors)


class FlockInspectionRecordSerializerTestCase(TestCase):
    """
    Test case for the FlockInspectionRecordSerializer.

    This test case verifies the serialization and deserialization of flock inspection records.

    """

    def setUp(self):
        """
        Set up the test case by creating housing structures, a flock, and valid data.

        """
        self.from_structure: HousingStructure = HousingStructure.objects.create(
            type=HousingStructureTypeChoices.Deep_Litter_House,
            category=HousingStructureCategoryChoices.Growers_House
        )
        self.to_structure: HousingStructure = HousingStructure.objects.create(
            type=HousingStructureTypeChoices.Deep_Litter_House,
            category=HousingStructureCategoryChoices.Growers_House
        )
        self.flock_source: FlockSource = FlockSource.objects.create(source=FlockSourceChoices.Kiplels_Farm)
        self.flock: Flock = Flock.objects.create(
            source=self.flock_source,
            date_of_hatching=date.today() - timedelta(weeks=9),
            chicken_type=ChickenTypeChoices.Layers,
            initial_number_of_birds=100,
            current_rearing_method=RearingMethodChoices.Cage_System,
            current_housing_structure=self.from_structure,
        )
        self.valid_data = {
            'flock': self.flock.id
        }

    def test_valid_serialization(self):
        """
        Test the serialization of valid flock inspection record data.

        - Create a flock inspection record serializer with valid data.
        - Validate the serializer.

        """
        serializer = FlockInspectionRecordSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_serialization(self):
        """
        Test the serialization of invalid flock inspection record data.

        - Create a flock inspection record serializer with invalid data.
        - Validate the serializer and check for errors.

        """
        invalid_data = {
            'flock': 9999
        }
        serializer = FlockInspectionRecordSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())


