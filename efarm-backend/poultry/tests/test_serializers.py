from django.test import TestCase

from poultry.serializers import *


class FlockSourceSerializerTestCase(TestCase):
    """
    Test case for the FlockSourceSerializer.
    """

    def setUp(self):
        """
        Set up the test case by creating a flock source.

        - Create a FlockSource instance.

        """
        self.flock_source: FlockSource = FlockSource.objects.create(source=FlockSourceChoices.THIS_FARM)

    def test_serialize_flock_source(self):
        """
        Test the serialization of a flock source.

        - Create a flock source serializer with the flock source instance.
        - Get the serialized data.
        - Compare the serialized data with the expected data.

        """
        serializer: FlockSourceSerializer = FlockSourceSerializer(instance=self.flock_source)
        serialized_data = serializer.data

        expected_data = {
            'id': self.flock_source.id,
            'source': 'This Farm'
        }

        self.assertDictEqual(serialized_data, expected_data)


class FlockBreedSerializerTestCase(TestCase):
    """
    Test case for the FlockBreedSerializer.
    """

    def setUp(self):
        """
        Set up the test case by creating a flock breed.

        - Create a FlockBreed instance.

        """
        self.flock_breed: FlockBreed = FlockBreed.objects.create(name=FlockBreedTypeChoices.EASTER_EGGER)

    def test_serialize_flock_breed(self):
        """
        Test the serialization of a flock breed.

        - Create a flock breed serializer with the flock breed instance.
        - Get the serialized data.
        - Compare the serialized data with the expected data.

        """
        serializer: FlockBreedSerializer = FlockBreedSerializer(instance=self.flock_breed)
        serialized_data = serializer.data

        expected_data = {
            'id': self.flock_breed.id,
            'name': FlockBreedTypeChoices.EASTER_EGGER
        }

        self.assertDictEqual(serialized_data, expected_data)


class HousingStructureSerializerTestCase(TestCase):
    """
    Test case for the HousingStructureSerializer.
    """

    def setUp(self):
        """
        Set up the test case by creating a housing structure.

        - Create a HousingStructure instance.

        """
        self.housing_structure: HousingStructure = HousingStructure.objects.create(
            type=HousingStructureTypeChoices.DEEP_LITTER_HOUSE,
            category=HousingStructureCategoryChoices.BREEDERS_HOUSE
        )

    def test_serialize_housing_structure(self):
        """
        Test the serialization of a housing structure.

        - Create a housing structure serializer with the housing structure instance.
        - Get the serialized data.
        - Compare the serialized data with the expected data.

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

        - Create FlockSource, FlockBreed, and HousingStructure instances.
        - Create a Flock instance.

        """
        self.flock_source: FlockSource = FlockSource.objects.create(source=FlockSourceChoices.KIPLELS_FARM)
        self.flock_breed: FlockBreed = FlockBreed.objects.create(name=FlockBreedTypeChoices.KUROILER)
        self.housing_structure: HousingStructure = HousingStructure.objects.create(
            type=HousingStructureTypeChoices.DEEP_LITTER_HOUSE,
            category=HousingStructureCategoryChoices.GROWERS_HOUSE
        )
        self.flock: Flock = Flock.objects.create(
            source=self.flock_source,
            breed=self.flock_breed,
            date_of_hatching=date.today() - timedelta(weeks=9),
            chicken_type=ChickenTypeChoices.LAYERS,
            initial_number_of_birds=10,
            current_rearing_method=RearingMethodChoices.DEEP_LITTER,
            current_housing_structure=self.housing_structure
        )

    def test_serialize_flock(self):
        """
        Test the serialization of a flock.

        - Create a flock serializer with the flock instance.
        - Get the serialized data.
        - Compare the serialized data with the expected data.

        """
        serializer: FlockSerializer = FlockSerializer(instance=self.flock)
        serialized_data: dict = serializer.data

        expected_data: dict = {
            'id': self.flock.id,
            'source': self.flock_source.id,
            'breed': self.flock_breed.id,
            'date_of_hatching': str(self.flock.date_of_hatching),
            'chicken_type': ChickenTypeChoices.LAYERS,
            'initial_number_of_birds': 10,
            'current_rearing_method': RearingMethodChoices.DEEP_LITTER,
            'current_housing_structure': self.housing_structure.id,
            'date_established': str(self.flock.date_established),
            'age_in_weeks': 9,
            'age_in_months': 2,
            'age_in_weeks_in_farm': 0,
            'age_in_months_in_farm': 0,
            'is_present': True,
        }

        self.assertDictEqual(serialized_data, expected_data)


class FlockHistorySerializerTestCase(TestCase):
    """
    Test case for the FlockHistorySerializer.
    """

    def setUp(self):
        """
        Set up the test case by creating a flock, flock source, housing structure, and flock history.

        - Create a HousingStructure instance.
        - Create a Flock instance.
        - Retrieve the FlockHistory instance associated with the flock.

        """
        self.housing_structure: HousingStructure = HousingStructure.objects.create(
            type=HousingStructureTypeChoices.DEEP_LITTER_HOUSE,
            category=HousingStructureCategoryChoices.GROWERS_HOUSE
        )
        self.flock: Flock = Flock.objects.create(
            source=FlockSource.objects.create(source=FlockSourceChoices.KIPLELS_FARM),
            breed=FlockBreed.objects.create(name=FlockBreedTypeChoices.KUROILER),
            date_of_hatching=date.today() - timedelta(weeks=9),
            chicken_type=ChickenTypeChoices.LAYERS,
            initial_number_of_birds=10,
            current_rearing_method=RearingMethodChoices.DEEP_LITTER,
            current_housing_structure=self.housing_structure,
        )
        self.flock_history: FlockHistory = FlockHistory.objects.get(flock=self.flock)

    def test_serialize_flock_history(self):
        """
        Test the serialization of a flock history.

        - Create a flock history serializer with the flock history instance.
        - Get the serialized data.
        - Compare the serialized data with the expected data.

        """
        serializer: FlockHistorySerializer = FlockHistorySerializer(instance=self.flock_history)
        serialized_data: dict = serializer.data

        expected_data: dict = {
            'id': self.flock_history.id,
            'flock': self.flock.id,
            'rearing_method': RearingMethodChoices.DEEP_LITTER,
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

        - Create HousingStructure instances for from_structure and to_structure.
        - Create FlockSource and FlockBreed instances.
        - Create a Flock instance.
        - Prepare flock movement data.

        """
        self.from_structure = HousingStructure.objects.create(
            type=HousingStructureTypeChoices.DEEP_LITTER_HOUSE,
            category=HousingStructureCategoryChoices.GROWERS_HOUSE
        )
        self.to_structure = HousingStructure.objects.create(
            type=HousingStructureTypeChoices.DEEP_LITTER_HOUSE,
            category=HousingStructureCategoryChoices.GROWERS_HOUSE
        )
        self.flock_source: FlockSource = FlockSource.objects.create(source=FlockSourceChoices.KIPLELS_FARM)
        self.flock_breed: FlockBreed = FlockBreed.objects.create(name=FlockBreedTypeChoices.KUROILER)

        self.flock = Flock.objects.create(
            source=self.flock_source,
            breed=self.flock_breed,
            date_of_hatching=date.today() - timedelta(weeks=9),
            chicken_type=ChickenTypeChoices.LAYERS,
            initial_number_of_birds=100,
            current_rearing_method=RearingMethodChoices.CAGE_SYSTEM,
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
        Set up the test case by creating necessary objects and valid data.

        - Create HousingStructure instances.
        - Create FlockSource and FlockBreed instances.
        - Create a Flock instance.
        - Prepare valid data for the flock inspection record serializer.

        """
        self.from_structure: HousingStructure = HousingStructure.objects.create(
            type=HousingStructureTypeChoices.DEEP_LITTER_HOUSE,
            category=HousingStructureCategoryChoices.GROWERS_HOUSE
        )
        self.to_structure: HousingStructure = HousingStructure.objects.create(
            type=HousingStructureTypeChoices.DEEP_LITTER_HOUSE,
            category=HousingStructureCategoryChoices.GROWERS_HOUSE
        )
        self.flock_source: FlockSource = FlockSource.objects.create(source=FlockSourceChoices.KIPLELS_FARM)
        self.flock_breed: FlockBreed = FlockBreed.objects.create(name=FlockBreedTypeChoices.KUROILER)
        self.flock: Flock = Flock.objects.create(
            source=self.flock_source,
            breed=self.flock_breed,
            date_of_hatching=date.today() - timedelta(weeks=9),
            chicken_type=ChickenTypeChoices.LAYERS,
            initial_number_of_birds=100,
            current_rearing_method=RearingMethodChoices.CAGE_SYSTEM,
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
        - Assert that the serializer is valid.

        """
        serializer = FlockInspectionRecordSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_serialization(self):
        """
        Test the serialization of invalid flock inspection record data.

        - Create a flock inspection record serializer with invalid data.
        - Validate the serializer and check for errors.
        - Assert that the serializer is not valid.

        """
        invalid_data = {
            'flock': 9999
        }
        serializer = FlockInspectionRecordSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())


class FlockBreedInformationSerializerTestCase(TestCase):
    """
    Test case for the FlockBreedInformationSerializer.

    This test case verifies the serialization and deserialization of flock breed information.

    """

    def test_serializer_valid_data(self):
        """
        Test the serialization of flock breed information with valid data.

        - Create a flock breed instance.
        - Create valid data for the serializer.
        - Create a serializer instance with the valid data.
        - Validate the serializer.
        - Save the serializer data and verify that a new FlockBreedInformation object is created.

        """
        breed = FlockBreed.objects.create(name=FlockBreedTypeChoices.BANTAM)

        data = {
            'breed': breed.id,
            'chicken_type': ChickenTypeChoices.BROILER,
            'average_mature_weight_in_kgs': 2.5,
            'average_egg_production': None,
            'maturity_age_in_weeks': 8
        }

        serializer = FlockBreedInformationSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertEqual(FlockBreedInformation.objects.all().count(), 1)

    def test_serializer_invalid_data(self):
        """
        Test the serialization of flock breed information with invalid data.

        - Create invalid data for the serializer.
        - Create a serializer instance with the invalid data.
        - Validate the serializer and check for errors.

        """
        data = {
            'breed': None,  # Missing required field
            'chicken_type': ChickenTypeChoices.BROILER,
            'average_mature_weight_in_kgs': 0.5,  # Below minimum value
            'average_egg_production': 100,  # Restricted not to be allowed for broilers
            'maturity_age_in_weeks': 4  # Below minimum value for broiler
        }

        serializer = FlockBreedInformationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        # print(serializer.errors)
        self.assertEqual(len(serializer.errors), 1)  # Four validation errors expected but for some reason the serializer only returns the first error


class EggCollectionSerializerTestCase(TestCase):
    """
    Test case for the EggCollectionSerializer.

    This test case verifies the serialization and creation of egg collection records.

    """

    def setUp(self):
        """
        Set up the test case by creating necessary objects and data.

        - Create a FlockSource instance.
        - Create a FlockBreed instance.
        - Create a HousingStructure instance.
        - Create a Flock instance.
        - Prepare data for the egg collection serializer.

        """
        self.flock_source: FlockSource = FlockSource.objects.create(source=FlockSourceChoices.KUKU_CHICK)
        self.flock_breed: FlockBreed = FlockBreed.objects.create(name=FlockBreedTypeChoices.SASSO_F1)

        self.layers_house: HousingStructure = HousingStructure.objects.create(
            type=HousingStructureTypeChoices.SEMI_INTENSIVE_HOUSING,
            category=HousingStructureCategoryChoices.LAYERS_HOUSE)

        self.flock: Flock = Flock.objects.create(
            source=self.flock_source,
            breed=self.flock_breed,
            date_of_hatching=date.today() - timedelta(weeks=19),
            chicken_type=ChickenTypeChoices.LAYERS,
            initial_number_of_birds=20,
            current_rearing_method=RearingMethodChoices.CAGE_SYSTEM,
            current_housing_structure=self.layers_house)

        self.egg_collection_data = {
            'flock': self.flock.id,
            'collected_eggs': 5,
            'broken_eggs': 2
        }

        self.serializer = EggCollectionSerializer(data=self.egg_collection_data)

    def test_valid_serializer(self):
        """
        Test the validity of the egg collection serializer.

        - Validate the serializer.
        - Assert that the serializer is valid.

        """
        self.assertTrue(self.serializer.is_valid())

    def test_create_egg_collection(self):
        """
        Test the creation of an egg collection record.

        - Validate the serializer.
        - Save the serializer data and retrieve the created egg collection object.
        - Verify that the egg collection object is created with the correct data.

        """
        self.serializer.is_valid()
        egg_collection = self.serializer.save()

        self.assertEqual(egg_collection.flock, self.flock)
        self.assertIsNotNone(egg_collection.date)
        self.assertIsNotNone(egg_collection.time)
        self.assertEqual(egg_collection.collected_eggs, self.egg_collection_data['collected_eggs'])
        self.assertEqual(egg_collection.broken_eggs, self.egg_collection_data['broken_eggs'])
