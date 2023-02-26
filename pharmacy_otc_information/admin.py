from django.contrib import admin

# Register your models here.

from .models import DrugEfficacyClassification, PharmacyOTCInformation

# Register your models here.
admin.site.register(DrugEfficacyClassification)
admin.site.register(PharmacyOTCInformation)
# admin.site.register(PharmacyOTCDetial)
