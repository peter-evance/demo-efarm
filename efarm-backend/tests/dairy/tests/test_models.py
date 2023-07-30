from pprint import pprint

import pytest

from dairy.models import *
from dairy.serializers import *
from tests.dairy.tests.test_rules import *


@pytest.mark.django_db
class TestCowModel:
    def test_cow_creation(self):
        serializer = CowSerializer(data={
            'name': 'General Cow',
            'breed': {'name': CowBreedChoices.AYRSHIRE},
            'date_of_birth': todays_date - timedelta(days=200),
            'gender': SexChoices.FEMALE,
            'availability_status': CowAvailabilityChoices.ALIVE,
            'current_pregnancy_status': CowPregnancyChoices.UNAVAILABLE,
            'category': CowCategoryChoices.HEIFER,
            'current_production_status': CowProductionStatusChoices.YOUNG_HEIFER
        })
        assert serializer.is_valid()
        cow = serializer.save()

        assert cow.tag_number is not None
        assert cow.name == 'General Cow'
        assert cow.breed.name == CowBreedChoices.AYRSHIRE
        assert cow.date_of_birth == todays_date - timedelta(days=200)
        assert cow.gender == SexChoices.FEMALE
        assert cow.availability_status == CowAvailabilityChoices.ALIVE
        assert cow.current_pregnancy_status == CowPregnancyChoices.UNAVAILABLE
        assert cow.category == CowCategoryChoices.HEIFER
        assert cow.current_production_status == CowProductionStatusChoices.YOUNG_HEIFER

        # Ensure that sire and dam are initially set to None
        assert cow.sire is None
        assert cow.dam is None

        # Ensure that is_bought is initially set to False
        assert not cow.is_bought

        # Ensure that age, parity, and age_in_farm are calculated correctly
        assert cow.age == 200
        assert cow.parity == 0
        assert cow.age_in_farm == 0


@pytest.mark.django_db
class TestCowBreedModel:

    def test_valid_breed_creation(self):
        for breed_name, breed_data in cow_breed_rules.items():
            cow_breed = CowBreed.objects.create(**breed_data)
            assert cow_breed.name == breed_data['name']

    def test_duplicate_breed_name(self):
        guernsey_breed = CowBreed.objects.create(name=CowBreedChoices.GUERNSEY)
        duplicate_guernsey = CowBreed(name=CowBreedChoices.GUERNSEY)
        with pytest.raises(ValidationError) as context:
            duplicate_guernsey.save()
        assert f"A breed with the name '{duplicate_guernsey.name}' already exists." in context.value

    def test_invalid_breed_name(self):
        cow_breed = CowBreed(name='Test Invalid Breed')
        with pytest.raises(ValidationError) as context:
            cow_breed.save()
        assert f"Invalid cow breed: '{cow_breed.name}'." in context.value

# @pytest.mark.django_db
# def test_cow_creation():
#     # Define cow data
#     cow_data = cow_rules['general_cow']
#
#     # Create a cow breed
#     breed = CowBreed(name=cow_data['breed'])
#     breed.save()
#
#     # Assign the breed instance to the cow data
#     cow_data['breed'] = breed
#
#     # Create a cow
#     cow = Cow.objects.create(**cow_data)
#
#     # Assert cow attributes
#     assert cow.name == cow_data['name']
#     assert cow.breed == cow_data['breed']
#     assert cow.date_of_birth == cow_data['date_of_birth']
#     assert cow.gender == cow_data['gender']
#     assert cow.availability_status == cow_data['availability_status']
#     assert cow.current_pregnancy_status == cow_data['current_pregnancy_status']
#     assert cow.category == cow_data['category']
#     assert cow.current_production_status == cow_data['current_production_status']
#
#
# @pytest.mark.django_db
# def test_older_cow_creation():
#     # Define cow data
#     cow_data = cow_rules['older_cow']
#
#     # Create a cow breed
#     breed = CowBreed(name=cow_data['breed'])
#     breed.save()
#
#     # Assign the breed instance to the cow data
#     cow_data['breed'] = breed
#
#     with pytest.raises(ValidationError) as context:
#         old_cow: Cow = Cow.objects.create(**cow_data)
#         assert f"Cow cannot be older than 7 years! Current age specified: {old_cow.age / 365} years" in context.value
#
#
# @pytest.mark.django_db
# def test_future_cow_creation():
#     CowBreed.objects.all().delete()
#     Cow.objects.all().delete()
#     # Define cow data
#     cow_data = cow_rules['future_cow']
#
#     # Create a cow breed
#     breed = CowBreed(name=cow_data['breed'])
#     breed.save()
#
#     # Assign the breed instance to the cow data
#     cow_data['breed'] = breed
#
#     with pytest.raises(ValidationError) as context:
#         old_cow: Cow = Cow(**cow_data)
#         old_cow.save()
#     assert f"Date of birth cannot be in the future. You entered {old_cow.date_of_birth}" in context.value
#
#
# @pytest.mark.django_db
# def test_date_of_death_validation():
#     # Define cow data
#     cow_data = cow_rules['general_cow']
#
#     # Create a cow breed
#     breed = CowBreed(name=cow_data['breed'])
#     breed.save()
#
#     # # Assign the breed instance to the cow data
#     cow_data['breed'] = breed
#
#     cow_data['availability_status'] = CowAvailabilityChoices.DEAD
#
#     # Invalid case: Date of death not provided
#     with pytest.raises(ValidationError) as context:
#         cow: Cow = Cow(**cow_data)
#         cow.save()
#     assert "Sorry, this cow died! Update its status by adding the date of death." in context.value
#
#     # Invalid case: Date of death in the future
#     cow_data['date_of_death'] = todays_date + timedelta(days=1)  # Date of death to tomorrow
#     with pytest.raises(ValidationError) as context:
#         cow: Cow = Cow(**cow_data)
#         cow.save()
#     assert f"Date of death cannot be in the future. You entered {cow.date_of_death}" in context.value
#
#     # Invalid case: Date of death exceeds 24 hours from current date
#     cow_data['date_of_death'] = todays_date - timedelta(days=2)  # Set date of death 2 days ago
#     with pytest.raises(ValidationError) as context:
#         cow: Cow = Cow(**cow_data)
#         cow.save()
#     assert "Date of death entries longer than 24 hours ago are not allowed." in context.value
#
#     # Valid case: Date of death provided and within valid range
#     cow_data['date_of_death'] = todays_date - timedelta(days=1)  # Set date of death to yesterday
#     cow: Cow = Cow(**cow_data)
#     cow.save()
#
#
# @pytest.mark.django_db
# def test_pregnancy_status_validation():
#     CowBreed.objects.all().delete()
#     Cow.objects.all().delete()
#
#     # Define cow data
#     cow_data = cow_rules['under_one_year_old_heifer']
#
#     # Create a cow breed
#     breed = CowBreed(name=cow_data['breed'])
#     breed.save()
#
#     # Assign the breed instance to the cow data
#     cow_data['breed'] = breed
#
#     # Set age to less than 12 months and pregnancy status to 'Pregnant'
#     cow_data['current_pregnancy_status'] = CowPregnancyChoices.PREGNANT
#
#     # Attempt to create the cow and expect a validation error
#     with pytest.raises(ValidationError) as context:
#         cow: Cow = Cow.objects.create(**cow_data)
#         print(context.value)
#
#     # Check if the validation error message is as expected assert f"Cows must be 12 months or older to be set as
#     # pregnant or open.
#     # Current age: {cow.age / 30.42} months."
#     # in context.value
#
#     # Set age to 12 months and pregnancy status to 'Pregnant'
#     cow_data['date_of_birth'] = todays_date - timedelta(days=366)  # 12 months
#
#     # Create the cow and expect no validation error
#     cow: Cow = Cow.objects.create(**cow_data)
#
#     # Check if the cow is created successfully
#     assert cow is not None

# @pytest.mark.django_db
# def test_gender_update_validation():
#     CowBreed.objects.all().delete()
#     Cow.objects.all().delete()
#
#     # Define cow data
#     cow_data = cow_rules['general_cow']
#
#     # Create a cow breed
#     breed_name = cow_data['breed']
#     breed = CowBreed.objects.create(name=breed_name)
#
#     # Assign the breed instance to the cow data
#     cow_data['breed'] = breed_name
#
#     # Create a cow with the initial gender
#     cow = Cow.objects.create(**cow_data)
#
#     # Attempt to update the cow's gender to a different value
#     with pytest.raises(ValidationError) as context:
#         cow.gender = SexChoices.MALE
#         cow.save()
#
#     # Check if the validation error message is as expected
#     assert "Cannot update the gender of the cow" in str(context.value)
#
#     # Update the cow's gender to the same value
#     cow.gender = SexChoices.FEMALE
#     cow.save()
#
#     # Check if the cow is updated successfully
#     assert cow.gender == SexChoices.FEMALE
