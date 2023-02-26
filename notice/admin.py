from django.contrib import admin
from notice.models import Notice, NotificeDeliveryChoices,NotificeStatusChoices
# Register your models here.
admin.site.register(Notice)
admin.site.register(NotificeStatusChoices)
admin.site.register(NotificeDeliveryChoices)
