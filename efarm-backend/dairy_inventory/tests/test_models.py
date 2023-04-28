from django.test import TestCase
from datetime import date, timedelta
from dairy.models import Cow, Milk, Pregnancy
from dairy_inventory.models import *


class MilkInventoryModelTestCase(TestCase):
    def setUp(self):
        self.cow = Cow.objects.create(name='Daisy',
                                      breed='Friesian',
                                      date_of_birth=date.today() - timedelta(days=1460),
                                      gender='Female',
                                      pregnancy_status='Not Pregnant')
        self.pregnancy = Pregnancy.objects.create(cow=self.cow,
                                                  start_date=date.today() - timedelta(days=300),
                                                  date_of_calving=date.today() - timedelta(days=15),
                                                  pregnancy_status='Confirmed',
                                                  pregnancy_outcome='Live')
        self.milk_record = Milk.objects.create(cow=self.cow,
                                               amount_in_kgs=20.5,
                                               lactation=self.cow.lactation_set.last())

    def test_milk_inventory_creation(self):
        milk_inventory = MilkInventory.objects.get(id=1)
        self.assertEqual(milk_inventory.total_amount_in_kgs, 20.5)

    def test_milk_inventory_update_history_creation(self):
        milk_inventory = MilkInventory.objects.get(id=1)
        self.assertEqual(milk_inventory.total_amount_in_kgs, 20.5)
        milk_update_history = MilkInventoryUpdateHistory.objects.get(id=1)
        self.assertEqual(milk_update_history.amount_in_kgs_change, 20.5)
        self.assertEqual(milk_update_history.update_type, MilkInventoryUpdateHistory.UpdateType.ADD)
        self.assertEqual(milk_update_history.amount_in_kgs, 20.5)
