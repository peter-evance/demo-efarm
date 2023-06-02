from datetime import date, datetime, timedelta
from django.contrib.admin.sites import AdminSite

from django.urls import path
from django.contrib import admin
from django.db.models import functions, Count, Sum
from django.template.response import TemplateResponse
from . import models


class HeatAdmin(admin.ModelAdmin):
    list_display = ("observation_time", "cow")


class CowAdmin(admin.ModelAdmin):
    list_display = ("name", "breed", "tag_number", "milk_records", "age", "date_of_birth", "pregnancy_status", "gender")
    list_display_links = ("name", "breed", "tag_number", "milk_records")
    list_filter = ("breed", "date_of_birth")
    search_fields = ("name",)
    date_hierachy = "date_of_birth",

    def milk_records(self, obj):
        return obj.milk.count()


class EmployeesCowAdmin(admin.ModelAdmin):
    read_only_fields = ("name", "breed", "tag_number")


class LactationAdmin(admin.ModelAdmin):
    list_display = ("lactation_stage", "start_date", "end_date_", "lactation_duration", "cow")
    list_filter = ("start_date",)
    readonly_fields = ("lactation_stage", "start_date", "end_date_", "lactation_duration", "cow")


class InseminatorAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone_number", "company", "license_number")


class PregnancyAdmin(admin.ModelAdmin):
    list_display = ("cow", "start_date", "date_of_calving", "pregnancy_duration", "due_date", "latest_lactation_stage")
    list_filter = ("date_of_calving",)


class MilkAdmin(admin.ModelAdmin):
    list_display = ('milking_date', 'amount_in_kgs', 'lactation_stage', 'cow')
    list_filter = ('milking_date',)

    def lactation_stage(self, obj):
        lactation = obj.cow.lactation_set.latest()
        if not lactation:
            return 'No lactation'
        if lactation.lactation_stage == 'Dry':
            return 'Dried off'
        return lactation.lactation_stage


class WeightRecordAdmin(admin.ModelAdmin):
    list_display = ('cow', 'weight', 'date')


class DiseaseAdmin(admin.ModelAdmin):
    list_display = ("name", "pathogen", "categories", "is_recovered")
    list_filter = ("categories", "pathogen", "cows")
    search_fields = ("name",)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.symptoms.set(form.cleaned_data['symptoms'])
        obj.treatments.set(form.cleaned_data['treatments'])


class SymptomsAdmin(admin.ModelAdmin):
    list_display = ("name", "severity", "type", "date_observed")


class TreatmentAdmin(admin.ModelAdmin):
    list_display = ("date_of_treatment", "treatment_method", "treatment_status", "cow",)
    list_filter = ("disease", "date_of_treatment", "treatment_status")


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


class BarnAdmin(admin.ModelAdmin):
    list_display = ("name", 'capacity')


class CowProductionStatusAdmin(admin.ModelAdmin):
    list_display = ("name",)


class CowPenAdmin(admin.ModelAdmin):
    list_display = ('barn', 'category', 'type', 'capacity')


admin.site.register(models.Heat, HeatAdmin)
admin.site.register(models.Insemination, InseminationAdmin)
admin.site.register(models.Treatment, TreatmentAdmin)
admin.site.register(models.Disease, DiseaseAdmin)
admin.site.register(models.Cow, CowAdmin)
admin.site.register(models.Milk, MilkAdmin)
admin.site.register(models.Lactation, LactationAdmin)
admin.site.register(models.Pregnancy, PregnancyAdmin)
admin.site.register(models.Inseminator, InseminatorAdmin)
admin.site.register(models.Semen, SemenAdmin)
admin.site.register(models.Symptoms, SymptomsAdmin)
admin.site.register(models.Culling, CullingAdmin)
admin.site.register(models.WeightRecord, WeightRecordAdmin)
admin.site.register(models.Pathogen, PathogenAdmin)
admin.site.register(models.DiseaseCategory, DiseaseCategoryAdmin)
admin.site.register(models.Barn, BarnAdmin)
admin.site.register(models.CowPen, CowPenAdmin)
