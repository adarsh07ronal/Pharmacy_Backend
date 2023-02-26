from django.contrib import admin
from message.models import ReservationMessage, TemplateReservationMessage, UserMemoMessage

# Register your models here.

admin.site.register(ReservationMessage)
admin.site.register(TemplateReservationMessage)
admin.site.register(UserMemoMessage)