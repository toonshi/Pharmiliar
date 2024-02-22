# Register your models here.
from django.contrib import admin
from .models import Service, Insurance, Institution

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('service_name', 'service_price')

@admin.register(Insurance)
class InsuranceAdmin(admin.ModelAdmin):
    list_display = ('insurance_name', 'institution')

@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('institution_name',  'phone_number', 'image')
