# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from drug.models import Medicine,MedicineEfficacyClassification

# Register your models here.
admin.site.register(Medicine)
admin.site.register(MedicineEfficacyClassification)