from django.contrib import admin
from .models import *


class MilkInventoryUpdateHistoryModelAdmin(admin.ModelAdmin):
    list_display = ('date', 'amount_in_kgs')


class CowInventoryModelAdmin(admin.ModelAdmin):
    list_display = ('total_number_of_cows', 'number_of_female_cows', 'number_of_male_cows',
                    'number_of_sold_cows', 'number_of_dead_cows')


class CowInventoryUpdateHistoryModelAdmin(admin.ModelAdmin):
    list_display = ('number_of_cows', 'date')


class BarnInventoryModelAdmin(admin.ModelAdmin):
    list_display = ('barn',)


class CowPenInventoryModelAdmin(admin.ModelAdmin):
    list_display = ('pen','number_of_cows')


admin.site.register(CowInventory, CowInventoryModelAdmin)
admin.site.register(CowInventoryUpdateHistory, CowInventoryUpdateHistoryModelAdmin)
admin.site.register(MilkInventory)
admin.site.register(MilkInventoryUpdateHistory, MilkInventoryUpdateHistoryModelAdmin)
admin.site.register(BarnInventory, BarnInventoryModelAdmin)
admin.site.register(CowPenInventory, CowPenInventoryModelAdmin)
