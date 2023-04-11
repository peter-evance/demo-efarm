from django.contrib import admin
from .models import *


class MilkInventoryUpdateHistoryModelAdmin(admin.ModelAdmin):
    list_display = ('date', 'amount_in_kgs', 'amount_in_kgs_change', 'update_type')


admin.site.register(MilkInventory)
admin.site.register(MilkInventoryUpdateHistory, MilkInventoryUpdateHistoryModelAdmin)
