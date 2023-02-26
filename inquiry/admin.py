from django.contrib import admin
from inquiry.models import Inquiry,InquiryMessage
# Register your models here.
admin.site.register(Inquiry)
admin.site.register(InquiryMessage)
