from datetime import timedelta

from django.test import TestCase
from poultry.serializers import *
from poultry.models import *
from poultry.choices import *


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
