from django.contrib import admin
from .models import *

# Register your models here.

class BreedAdmin(admin.ModelAdmin):
    list_display= ("name",)


class CowAdmin(admin.ModelAdmin):
    list_display= ("name", "breed", "tag_number", "milk_records","age", "date_of_birth", "gender" )
    list_display_links= ("name", "breed", "tag_number", "milk_records")
    list_filter= ("breed", "date_of_birth")
    search_fields= ("name",)
    date_hierachy= "date_of_birth",
    
    def milk_records(self,obj):
        return obj.milk.count()
    
    
class MilkAdmin(admin.ModelAdmin):
    list_display= ('milking_date', 'amount_in_kgs','lactation_stage', 'cow')
    list_filter= ('milking_date',)
    
    def lactation_stage(self, obj):
        lactation = obj.cow.lactation_set.latest()
        if not lactation:
            return 'No lactation'
        if lactation.lactation_stage == 'Dry':
            return 'Dried off'
        return lactation.lactation_stage
class LactationAdmin(admin.ModelAdmin):
    list_display= ("lactation_stage","start_date", "end_date_","lactation_duration", "cow")
    list_filter= ("start_date",)
    readonly_fields = ("lactation_stage","start_date", "end_date_","lactation_duration", "cow")
    
class PregnancyAdmin(admin.ModelAdmin):
    list_display = ("cow", "start_date", "date_of_calving", "pregnancy_duration","due_date")
    list_filter = ("date_of_calving",)
    
class WeightRecordAdmin(admin.ModelAdmin):
    list_display= ('cow','weight','date')
    
class HeatAdmin(admin.ModelAdmin):
    list_display= ('observation_time',)

admin.site.register(Cow, CowAdmin)
admin.site.register(Breed, BreedAdmin)
admin.site.register(Milk, MilkAdmin)
admin.site.register(Pregnancy, PregnancyAdmin)
admin.site.register(Lactation, LactationAdmin)
admin.site.register(WeightRecord, WeightRecordAdmin)
admin.site.register(Heat, HeatAdmin)