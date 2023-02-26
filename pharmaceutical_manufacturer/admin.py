from django.contrib import admin
from .models import PharmaceuticalManufacturer, PublicationPlace, PostingType

# Register your models here.
admin.site.register(PublicationPlace)
admin.site.register(PostingType)
admin.site.register(PharmaceuticalManufacturer)