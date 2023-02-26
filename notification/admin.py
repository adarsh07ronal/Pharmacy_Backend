from django.contrib import admin

# Register your models here.
from .models import Notification, EmailNotification

admin.site.register(Notification)
admin.site.register(EmailNotification)