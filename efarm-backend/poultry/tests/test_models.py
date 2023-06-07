from django.core.exceptions import ValidationError
from django.test import TestCase
from poultry.models import *
from poultry.choices import *
from datetime import date, timedelta


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
            type=HousingStructureTypeChoices.Deep_Litter_House,
            category=HousingStructureCategoryChoices.Brooder_Chick_House,
        )

        self.breeder_house_valid_type: HousingStructure = HousingStructure(
            type=HousingStructureTypeChoices.Semi_Intensive_Housing,
            category=HousingStructureCategoryChoices.Breeders_House,
        )

        self.breeder_house_invalid_type: HousingStructure = HousingStructure(
            type=HousingStructureTypeChoices.Pasture_Housing,
            category=HousingStructureCategoryChoices.Breeders_House,
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
            type=HousingStructureTypeChoices.Open_Sided_Shed,
            category=HousingStructureCategoryChoices.Brooder_Chick_House,
        )
        expected_error_message = "Brood and chick houses are limited to Deep Litter House or Closed Shed structure types."

        with self.assertRaisesMessage(ValidationError, expected_error_message):
            structure.clean()

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
        flock_source: FlockSource = FlockSource.objects.create(source=FlockSourceChoices.This_Farm)

        growers_house: HousingStructure = HousingStructure.objects.create(
            type=HousingStructureTypeChoices.Open_Sided_Shed,
            category=HousingStructureCategoryChoices.Growers_House,
        )
        layers_house: HousingStructure = HousingStructure.objects.create(
            type=HousingStructureTypeChoices.Closed_Shed,
            category=HousingStructureCategoryChoices.Layers_House,
        )
        broiler_house: HousingStructure = HousingStructure.objects.create(
            type=HousingStructureTypeChoices.Semi_Intensive_Housing,
            category=HousingStructureCategoryChoices.Broilers_House,
        )

        Flock.objects.create(
            source=flock_source,
            date_of_hatching=date.today() - timedelta(weeks=4),  # 4 weeks old
            chicken_type=ChickenTypeChoices.Broiler,
            initial_number_of_birds=100,
            current_rearing_method=RearingMethodChoices.Cage_System,
            current_housing_structure=broiler_house,
        )

        Flock.objects.create(
            source=flock_source,
            date_of_hatching=date.today() - timedelta(weeks=19),  # 19 weeks old
            chicken_type=ChickenTypeChoices.Layers,
            initial_number_of_birds=200,
            current_rearing_method=RearingMethodChoices.Free_Range,
            current_housing_structure=layers_house,
        )

        Flock.objects.create(
            source=flock_source,
            date_of_hatching=date.today() - timedelta(weeks=6),  # 6 weeks old
            chicken_type=ChickenTypeChoices.Multi_Purpose,
            initial_number_of_birds=50,
            current_rearing_method=RearingMethodChoices.Deep_Litter,
            current_housing_structure=growers_house,
        )

        self.broiler_flock: Flock = Flock.objects.get(chicken_type=ChickenTypeChoices.Broiler)
        self.layers_flock: Flock = Flock.objects.get(chicken_type=ChickenTypeChoices.Layers)
        self.multipurpose_flock: Flock = Flock.objects.get(chicken_type=ChickenTypeChoices.Multi_Purpose)

    def test_housing_structure_assignment(self):
        """
        Test the assignment of housing structures to flocks.

        Asserts that the housing structure assignment is correct based on flock type and age.
        """
        self.assertEqual(
            self.broiler_flock.current_housing_structure.category,
            HousingStructureCategoryChoices.Broilers_House
        )

        self.assertEqual(
            self.layers_flock.current_housing_structure.category,
            HousingStructureCategoryChoices.Layers_House
        )

        self.assertEqual(
            self.multipurpose_flock.current_housing_structure.category,
            HousingStructureCategoryChoices.Growers_House
        )

    def test_creation_of_flock_history(self):
        """
        Test the creation of flock history.

        Asserts that flock history is created for each flock.
        """
        broiler_flock_history: FlockHistory = FlockHistory.objects.get(flock=self.broiler_flock)
        layers_flock_history: FlockHistory = FlockHistory.objects.get(flock=self.layers_flock)
        multipurpose_flock_history: FlockHistory = FlockHistory.objects.get(flock=self.multipurpose_flock)

        self.assertIsNotNone(broiler_flock_history)
        self.assertIsNotNone(layers_flock_history)
        self.assertIsNotNone(multipurpose_flock_history)
