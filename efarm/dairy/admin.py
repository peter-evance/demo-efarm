from django.contrib import admin
from .models import *

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

class DiseaseAdmin(admin.ModelAdmin):
    list_display = ("name", "pathogen", "categories", "is_recovered")
    list_filter = ("categories", "pathogen", "cows")
    search_fields = ("name",)
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.symptoms.set(form.cleaned_data['symptoms'])
        obj.treatments.set(form.cleaned_data['treatments'])
    
class SymptomsAdmin(admin.ModelAdmin):
    list_display = ("name", "severity","type", "date_observed")

class TreatmentAdmin(admin.ModelAdmin):
    list_display = ("date_of_treatment", "treatment_method","treatment_status", "cow",)
    list_filter = ("disease", "date_of_treatment", "treatment_status")

class InseminatorAdmin(admin.ModelAdmin):
    list_display= ("name", "email", "phone_number" , "company", "license_number" )  
class InseminationAdmin(admin.ModelAdmin):
    list_display = ("date_of_insemination", "success", "days_since_insemination", "cow", "inseminator")
    list_filter = ("success", "date_of_insemination")
    
class SemenAdmin(admin.ModelAdmin):
    list_display = ("producer", "date_of_production", "date_of_expiry", "semen_batch",)
    list_filter = ("producer", "date_of_production")

class CullingAdmin(admin.ModelAdmin):
    list_display = ("cow", "reason")

class PathogenAdmin(admin.ModelAdmin):
    list_display = ("name",)

class DiseaseCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)


admin.site.register(Cow, CowAdmin)
admin.site.register(Milk, MilkAdmin)
admin.site.register(Pregnancy, PregnancyAdmin)
admin.site.register(Lactation, LactationAdmin)
admin.site.register(WeightRecord, WeightRecordAdmin)
admin.site.register(Heat, HeatAdmin)
admin.site.register(Pathogen, PathogenAdmin)
admin.site.register(DiseaseCategory, DiseaseCategoryAdmin)
admin.site.register(Inseminator, InseminatorAdmin)
admin.site.register(Semen,  SemenAdmin)
admin.site.register(Symptoms, SymptomsAdmin)
admin.site.register(Culling, CullingAdmin)
admin.site.register(Insemination, InseminationAdmin)
admin.site.register(Treatment, TreatmentAdmin)
admin.site.register(Disease, DiseaseAdmin)