from django.contrib import admin
from .models import *

# Register your models here.

class BreedAdmin(admin.ModelAdmin):
    list_display= ("name",)

class CowAdmin(admin.ModelAdmin):
    list_display= ("name","breed","tag_number","age")
    
    
class MilkAdmin(admin.ModelAdmin):
    list_display=("milking_date","milking_time","cow")
    
class LactationAdmin(admin.ModelAdmin):
    list_display= ("lactation_stage","start_date","lactation_duration", "cow")
    list_filter= ("start_date",)
    readonly_fields = ("lactation_stage","start_date","lactation_duration", "cow")
    
class PregnancyAdmin(admin.ModelAdmin):
    list_display = ("cow", "start_date", "date_of_calving", "pregnancy_duration","due_date")
    list_filter = ("date_of_calving",)

admin.site.register(Cow, CowAdmin)
admin.site.register(Breed, BreedAdmin)
admin.site.register(Milk, MilkAdmin)
admin.site.register(Pregnancy, PregnancyAdmin)
admin.site.register(Lactation, LactationAdmin)