from django.core.exceptions import ValidationError
from django.test import TestCase
from datetime import date, timedelta
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
        self.assertTrue("Sorry, this cow died! Update it's status by adding the date of death." in str(context.exception))

        # Ensure the validation error is raised if the cow's pregnancy status is set to "Pregnant" but she's less than 21 months old.
        self.cow2.availability_status = "Alive"
        self.cow2.pregnancy_status = "Pregnant"
        self.cow2.date_of_birth = date.today() - timedelta(weeks=5)
        with self.assertRaises(ValidationError) as context:
            self.cow2.clean()
        self.assertTrue("Cows must be 21 months or older to be set as pregnant" in str(context.exception))
    
            
