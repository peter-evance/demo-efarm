import pytest

from dairy.serializers import *


@pytest.mark.django_db
class TestCowBreedModel:

    def test_valid_breed_creation(self):
        cow_breed = CowBreed.objects.create(name=CowBreedChoices.GUERNSEY)
        assert cow_breed.name == CowBreedChoices.GUERNSEY

    def test_duplicate_breed_name(self):
        CowBreed.objects.create(name=CowBreedChoices.GUERNSEY)
        duplicate_guernsey = CowBreed(name=CowBreedChoices.GUERNSEY)
        with pytest.raises(ValidationError) as context:
            duplicate_guernsey.save()
        assert f"A breed with the name '{duplicate_guernsey.name}' already exists." in context.value

    def test_invalid_breed_name(self):
        cow_breed = CowBreed(name='Test Invalid Breed')
        with pytest.raises(ValidationError) as context:
            cow_breed.save()
        assert f"Invalid cow breed: '{cow_breed.name}'." in context.value
