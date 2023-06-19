from datetime import date, timedelta

from django.test import TestCase

from poultry.choices import *
from poultry.models import *


class HousingStructureTestCase(TestCase):
    """
    Test case for the HousingStructure model.

    Tests the validation of housing structure types and categories.
    """

    def setUp(self):
        """
        Set up the test case by creating different housing structures.
        """
        self.brooder_chick_house_valid_type: HousingStructure = HousingStructure(
            type=HousingStructureTypeChoices.DEEP_LITTER_HOUSE,
            category=HousingStructureCategoryChoices.BROODER_CHICK_HOUSE,
        )

        self.breeder_house_valid_type: HousingStructure = HousingStructure(
            type=HousingStructureTypeChoices.SEMI_INTENSIVE_HOUSING,
            category=HousingStructureCategoryChoices.BREEDERS_HOUSE,
        )

        self.breeder_house_invalid_type: HousingStructure = HousingStructure(
            type=HousingStructureTypeChoices.PASTURE_HOUSING,
            category=HousingStructureCategoryChoices.BREEDERS_HOUSE,
        )

    def test_brooder_chick_house_valid_type(self):
        """
        Test validation for a housing structure with a valid brooder chick house type.

        Asserts that no ValidationError is raised.
        """
        try:
            self.brooder_chick_house_valid_type.clean()
        except ValidationError:
            self.fail("Validation error raised for valid brooder chick house type.")

    def test_brooder_chick_house_invalid_type(self):
        """
        Test validation for a housing structure with an invalid brooder chick house type.

        Asserts that a ValidationError is raised with the correct error message.
        """
        structure: HousingStructure = HousingStructure(
            type=HousingStructureTypeChoices.OPEN_SIDED_SHED,
            category=HousingStructureCategoryChoices.BROODER_CHICK_HOUSE,
        )

        with self.assertRaisesMessage(ValidationError, "Brood and chick houses are limited to Deep Litter House or "
                                                       "Closed Shed structure types."):
            structure.save()

    def test_breeder_house_valid_type(self):
        """
        Test validation for a housing structure with a valid breeder house type.

        Asserts that no ValidationError is raised.
        """
        try:
            self.breeder_house_valid_type.clean()
        except ValidationError:
            self.fail("Validation error raised for valid breeder house type.")

    def test_breeder_house_invalid_type(self):
        """
        Test validation for a housing structure with an invalid breeder house type.

        Asserts that a ValidationError is raised.
        """
        with self.assertRaises(ValidationError):
            self.breeder_house_invalid_type.clean()


class FlockTestCase(TestCase):
    """
    Test case for the Flock model.

    Tests the functionality of flock creation and housing structure assignment.
    """

    def setUp(self):
        """
        Set up the test case by creating flock sources, housing structures, and flocks.
        """
        flock_source: FlockSource = FlockSource.objects.create(source=FlockSourceChoices.THIS_FARM)
        flock_breed: FlockBreed = FlockBreed.objects.create(name=FlockBreedTypeChoices.KUROILER)

        growers_house: HousingStructure = HousingStructure.objects.create(
            type=HousingStructureTypeChoices.OPEN_SIDED_SHED,
            category=HousingStructureCategoryChoices.GROWERS_HOUSE,
        )
        layers_house: HousingStructure = HousingStructure.objects.create(
            type=HousingStructureTypeChoices.CLOSED_SHED,
            category=HousingStructureCategoryChoices.LAYERS_HOUSE,
        )
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

        Flock.objects.create(
            source=flock_source,
            breed=flock_breed,
            date_of_hatching=date.today() - timedelta(weeks=19),  # 19 weeks old
            chicken_type=ChickenTypeChoices.LAYERS,
            initial_number_of_birds=200,
            current_rearing_method=RearingMethodChoices.FREE_RANGE,
            current_housing_structure=layers_house,
        )

        Flock.objects.create(
            source=flock_source,
            breed=flock_breed,
            date_of_hatching=date.today() - timedelta(weeks=6),  # 6 weeks old
            chicken_type=ChickenTypeChoices.MULTI_PURPOSE,
            initial_number_of_birds=50,
            current_rearing_method=RearingMethodChoices.DEEP_LITTER,
            current_housing_structure=growers_house,
        )

        self.broiler_flock: Flock = Flock.objects.get(chicken_type=ChickenTypeChoices.BROILER)
        self.layers_flock: Flock = Flock.objects.get(chicken_type=ChickenTypeChoices.LAYERS)
        self.multipurpose_flock: Flock = Flock.objects.get(chicken_type=ChickenTypeChoices.MULTI_PURPOSE)

    def test_housing_structure_assignment(self):
        """
        Test the assignment of housing structures to flocks.

        - Assert that the housing structure assignment is correct based on flock type and age.
        """
        self.assertEqual(
            self.broiler_flock.current_housing_structure.category,
            HousingStructureCategoryChoices.BROILERS_HOUSE
        )

        self.assertEqual(
            self.layers_flock.current_housing_structure.category,
            HousingStructureCategoryChoices.LAYERS_HOUSE
        )

        self.assertEqual(
            self.multipurpose_flock.current_housing_structure.category,
            HousingStructureCategoryChoices.GROWERS_HOUSE
        )

    def test_creation_of_flock_history(self):
        """
        Test the creation of flock history.

        - Assert that flock history is created for each flock.
        """
        broiler_flock_history: FlockHistory = FlockHistory.objects.get(flock=self.broiler_flock)
        layers_flock_history: FlockHistory = FlockHistory.objects.get(flock=self.layers_flock)
        multipurpose_flock_history: FlockHistory = FlockHistory.objects.get(flock=self.multipurpose_flock)

        self.assertIsNotNone(broiler_flock_history)
        self.assertIsNotNone(layers_flock_history)
        self.assertIsNotNone(multipurpose_flock_history)


class FlockMovementTestCase(TestCase):
    def setUp(self):
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

    def test_flock_movement_creation(self):
        """
        Test the creation of FlockMovement instance.

        - Assert that a FlockMovement instance is created successfully.

        """

        flock_movement = FlockMovement.objects.create(
            flock=self.flock,
            from_structure=self.from_structure,
            to_structure=self.to_structure
        )


class FlockInspectionRecordTestCase(TestCase):
    """
    Test case for the FlockInspectionRecord model.

    This test case verifies the creation and validation of flock inspection records.

    """

    def setUp(self):
        """
        Set up the test case by creating a flock, flock source, and a housing structure.

        """
        self.flock_source: FlockSource = FlockSource.objects.create(source=FlockSourceChoices.THIS_FARM)
        self.flock_breed: FlockBreed = FlockBreed.objects.create(name=FlockBreedTypeChoices.KUROILER)

        self.broiler_house: HousingStructure = HousingStructure.objects.create(
            type=HousingStructureTypeChoices.SEMI_INTENSIVE_HOUSING,
            category=HousingStructureCategoryChoices.BROILERS_HOUSE,
        )

        self.flock: Flock = Flock.objects.create(
            source=self.flock_source,
            breed=self.flock_breed,
            date_of_hatching=date.today() - timedelta(weeks=4),  # 4 weeks old
            chicken_type=ChickenTypeChoices.BROILER,
            initial_number_of_birds=100,
            current_rearing_method=RearingMethodChoices.CAGE_SYSTEM,
            current_housing_structure=self.broiler_house,
        )

    def test_valid_flock_inspection_record_creation(self):
        """
        Test the creation of a valid flock inspection record.

        - Create a flock inspection record for the flock.
        - Assert that the `is_present` field of the flock is False after the signal has been triggered.

        """
        FlockInspectionRecord.objects.create(flock=self.flock, number_of_dead_birds=100)

        self.flock.refresh_from_db()  # Refresh the flock instance from the database

        self.assertFalse(self.flock.is_present)  # Assert that `is_present` is False

    def test_model_validators(self):
        """
        Test the model validators of the flock inspection record.

        - Create a flock inspection record for the flock.
        - Try to create another flock inspection record for the same day around same time
        (should raise a ValidationError).
        - Try to create a fourth flock inspection record with a time separation greater than four hours
          from the previous inspection record (should raise a ValidationError).

        """

        # FlockInspectionRecord.objects.create(flock=self.flock)
        # FlockInspectionRecord.objects.create(flock=self.flock)
        # FlockInspectionRecord.objects.create(flock=self.flock)
        # FlockInspectionRecord.objects.create(flock=self.flock)

        with self.assertRaises(ValidationError):
            FlockInspectionRecord.objects.create(flock=self.flock,
                                                 number_of_dead_birds=101
                                                 )


class FlockBreedInformationTestCase(TestCase):
    def setUp(self):
        self.breed: FlockBreed = FlockBreed.objects.create(name=FlockBreedTypeChoices.INDIGENOUS)

    def test_clean_method(self):
        """
        Test the clean method of FlockBreedInformation model.

        - Test case when chicken_type is 'broiler' and average_egg_production is not null.
          Assert that the clean method raises a ValidationError.

        - Test case when chicken_type is 'broiler' and average_egg_production is null.
          Assert that no exception is raised.

        - Test case when chicken_type is not 'broiler' and average_egg_production is not null.
          Assert that no exception is raised.

        """

        flock_breed_info: FlockBreedInformation = FlockBreedInformation(
            breed=self.breed,
            chicken_type=ChickenTypeChoices.BROILER,
            average_mature_weight_in_kgs=1.75,
            average_egg_production=100,
            maturity_age_in_weeks=9
        )
        with self.assertRaises(ValidationError):
            flock_breed_info.clean()

        flock_breed_info.average_egg_production = None
        flock_breed_info.clean()  # No exception should be raised

        flock_breed_info.chicken_type = ChickenTypeChoices.LAYERS
        flock_breed_info.average_egg_production = 150
        flock_breed_info.maturity_age_in_weeks = 18
        flock_breed_info.clean()  # No exception should be raised

    def test_save_method(self):
        """
        Test the save method of FlockBreedInformation model.

        - Test case when saving a valid FlockBreedInformation instance.
          Assert that no exception is raised and the instance is saved.

        - Test case when saving an invalid FlockBreedInformation instance.
          Assert that the clean method raises a ValidationError and the instance is not saved.

        - Test case when saving an instance with null average_egg_production.
          Assert that no exception is raised and the instance is saved.

        """

        flock_breed_info: FlockBreedInformation = FlockBreedInformation(
            breed=self.breed,
            chicken_type=ChickenTypeChoices.LAYERS,
            average_mature_weight_in_kgs=2.0,
            average_egg_production=200,
            maturity_age_in_weeks=18
        )
        flock_breed_info.save()  # No exception should be raised
        self.assertEqual(FlockBreedInformation.objects.count(), 1)

        flock_breed_info: FlockBreedInformation = FlockBreedInformation(
            breed=self.breed,
            chicken_type=ChickenTypeChoices.BROILER,
            average_mature_weight_in_kgs=1.8,
            average_egg_production=100,
            maturity_age_in_weeks=9
        )
        with self.assertRaises(ValidationError):
            flock_breed_info.save()
        self.assertEqual(FlockBreedInformation.objects.count(), 1)  # The instance should not be saved

        flock_breed_info.average_egg_production = None
        flock_breed_info.save()  # No exception should be raised
        self.assertEqual(FlockBreedInformation.objects.count(), 2)


class EggCollectionModelTestCase(TestCase):
    """
    Test case for the EggCollection model.

    This test case verifies the creation and validation of egg collection records.

    """

    def setUp(self):
        """
        Set up the test case by creating a flock, flock source, and housing structures.

        """

        # Create the flock source, flock breed, and housing structures
        self.flock_source: FlockSource = FlockSource.objects.create(source=FlockSourceChoices.KUKU_CHICK)
        self.flock_breed: FlockBreed = FlockBreed.objects.create(name=FlockBreedTypeChoices.SASSO_F1)
        self.layers_house: HousingStructure = HousingStructure.objects.create(
            type=HousingStructureTypeChoices.SEMI_INTENSIVE_HOUSING,
            category=HousingStructureCategoryChoices.LAYERS_HOUSE,
        )
        self.growers_house: HousingStructure = HousingStructure.objects.create(
            type=HousingStructureTypeChoices.SEMI_INTENSIVE_HOUSING,
            category=HousingStructureCategoryChoices.GROWERS_HOUSE,
        )
        self.broiler_house: HousingStructure = HousingStructure.objects.create(
            type=HousingStructureTypeChoices.SEMI_INTENSIVE_HOUSING,
            category=HousingStructureCategoryChoices.BROILERS_HOUSE,
        )

        # Create the flock
        self.flock: Flock = Flock.objects.create(
            source=self.flock_source,
            breed=self.flock_breed,
            date_of_hatching=date.today() - timedelta(weeks=19),
            chicken_type=ChickenTypeChoices.LAYERS,
            initial_number_of_birds=20,
            current_rearing_method=RearingMethodChoices.CAGE_SYSTEM,
            current_housing_structure=self.layers_house
        )

    def test_clean_valid_data(self):
        """
        Test the clean method with valid data.

        - Create a valid egg collection with collected eggs and broken eggs counts.
        - Assert that the clean method does not raise any validation errors.

        """

        # Create a valid egg collection
        egg_collection = EggCollection(
            flock=self.flock,
            collected_eggs=10,
            broken_eggs=2
        )

        # Clean method should not raise any validation errors
        try:
            egg_collection.save()
        except ValidationError:
            self.fail("Unexpected ValidationError raised for valid data.")

    def test_clean_broken_eggs_greater_than_collected_eggs(self):
        """
        Test the clean method with broken eggs count greater than collected eggs count.

        - Create an egg collection with broken eggs count greater than collected eggs count.
        - Assert that the clean method raises a ValidationError with the expected error message.

        """

        # Create an egg collection with broken eggs greater than collected eggs
        egg_collection = EggCollection(
            flock=self.flock,
            collected_eggs=10,
            broken_eggs=15
        )

        # Clean method should raise a ValidationError
        with self.assertRaises(ValidationError) as context:
            egg_collection.save()

        self.assertIn(
            f"Broken eggs count ({egg_collection.broken_eggs}) cannot be greater than the collected eggs count "
            f"({egg_collection.collected_eggs})",
            context.exception
        )

    def test_clean_exceeds_collected_eggs_limit(self):
        """
        Test the clean method with collected eggs exceeding the limit for the day.

        - Create an egg collection exceeding the collected eggs limit for the day.
        - Assert that the clean method raises a ValidationError with the expected error message.

        """

        # Create an egg collection exceeding the collected eggs limit for the day
        EggCollection.objects.create(
            flock=self.flock,
            collected_eggs=10,
            broken_eggs=2
        )

        egg_collection = EggCollection(
            flock=self.flock,
            collected_eggs=21,
            broken_eggs=2
        )

        # Clean method should raise a ValidationError
        with self.assertRaises(ValidationError) as context:
            egg_collection.save()

        live_bird_count: int = self.flock.inventory.number_of_alive_birds
        total_collected_eggs: int = (
                EggCollection.objects.filter(flock=egg_collection.flock, date=egg_collection.date)
                .exclude(pk=egg_collection.pk)
                .aggregate(total=Sum('collected_eggs')).get('total') or 0
        )

        self.assertIn(
            f"Collected egg count for the day cannot exceed the count of living birds in the flock, "
            f"This flock has {live_bird_count} birds, and the collected eggs today must be "
            f"{live_bird_count - total_collected_eggs} or lower. The total collected eggs today is {total_collected_eggs}.",
            context.exception
        )

    def test_clean_exceeds_data_entry_limit(self):
        """
        Test the clean method with exceeding the data entry limit for the day.

        - Create multiple egg collections for the same flock and date.
        - Assert that the clean method raises a ValidationError with the expected error message.

        """

        # Create two egg collections for the same flock and date
        EggCollection.objects.create(
            flock=self.flock,
            collected_eggs=6,
            broken_eggs=1
        )
        EggCollection.objects.create(
            flock=self.flock,
            collected_eggs=6,
            broken_eggs=1
        )
        EggCollection.objects.create(
            flock=self.flock,
            collected_eggs=4,
            broken_eggs=1
        )
        egg_collection = EggCollection(
            flock=self.flock,
            collected_eggs=2,
            broken_eggs=1
        )

        # Clean method should raise a ValidationError
        with self.assertRaises(ValidationError) as context:
            egg_collection.save()

        tomorrow = timezone.now().astimezone(timezone.get_current_timezone()).date() + timezone.timedelta(days=1)
        self.assertIn(
            f"Data entry for this flock is limited to thrice per day. "
            f"Please try again on {tomorrow.strftime('%A %B %d, %Y')}.",
            context.exception
        )

    def test_clean_invalid_flock_chicken_type(self):
        """
        Test the clean method with an invalid flock chicken type.

        - Create an egg collection with an invalid flock chicken type.
        - Assert that the clean method raises a ValidationError with the expected error message.

        """

        flock = Flock.objects.create(
            source=self.flock_source,
            breed=self.flock_breed,
            date_of_hatching=date.today() - timedelta(weeks=10),
            chicken_type=ChickenTypeChoices.BROILER,
            initial_number_of_birds=20,
            current_rearing_method=RearingMethodChoices.CAGE_SYSTEM,
            current_housing_structure=self.broiler_house
        )

        egg_collection = EggCollection(
            flock=flock,
            collected_eggs=10,
            broken_eggs=2
        )

        # Clean method should raise a ValidationError
        with self.assertRaises(ValidationError) as context:
            egg_collection.save()

        self.assertIn(
            f"Egg collection is restricted to layers or multipurpose flocks, "
            f"You selected {flock.chicken_type.lower()}.",
            context.exception
        )

    def test_clean_invalid_flock_age(self):
        """
        Test the clean method with an invalid flock age.

        - Update the flock's age and housing structure.
        - Create an egg collection for the updated flock.
        - Assert that the clean method raises a ValidationError with the expected error message.

        """

        self.flock.date_of_hatching = date.today() - timedelta(weeks=13)
        self.flock.current_housing_structure = self.growers_house
        self.flock.save()

        egg_collection = EggCollection(
            flock=self.flock,
            collected_eggs=10,
            broken_eggs=5
        )

        # Clean method should raise a ValidationError
        with self.assertRaises(ValidationError) as context:
            egg_collection.save()

        self.assertIn(
            f"Egg collection is only allowed for flocks of age 14 weeks or older, "
            f"This flock is currently {self.flock.age_in_weeks} weeks old.",
            context.exception
        )

    def test_clean_invalid_flock_is_present(self):
        """
        Test the clean method with an invalid flock is_present field.

        - Create a flock inspection record indicating that the flock is not present.
        - Create an egg collection for the inspected flock.
        - Assert that the clean method raises a ValidationError with the expected error message.

        """

        FlockInspectionRecord.objects.create(flock=self.flock, number_of_dead_birds=20)
        self.flock.refresh_from_db()

        egg_collection = EggCollection(
            flock=self.flock,
            collected_eggs=10,
            broken_eggs=2
        )

        with self.assertRaises(ValidationError) as context:
            egg_collection.save()

        self.assertIn(
            f"Egg collection is only allowed for flocks marked as present. "
            f"This flock was marked not present on {self.flock.inventory.last_update.astimezone(timezone.get_current_timezone()).strftime('%A %B %d, %Y')}.",
            context.exception
        )
