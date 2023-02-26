from django.contrib import admin
from pharmacy_auth.models import User, Otp,AdministratorStatus
# Register your models here.

admin.site.register(User)
admin.site.register(Otp)
admin.site.register(AdministratorStatus)
