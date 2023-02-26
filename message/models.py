from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from reservation.models import ForReservation, UserMemo
from template.models import Template

User = get_user_model()

# Create your models here.

# Message Model used for Prescription Reciept reservation Chat

class ReservationMessage(models.Model):
    sender = models.ForeignKey(User,on_delete=models.CASCADE, related_name='reservation_sender_message')
    message = models.TextField(null=True,blank=True)
    is_seen_patient = models.BooleanField(default=True)
    is_seen_pharmacy = models.BooleanField(default=True)
    prescription_reservation = models.ForeignKey(ForReservation,on_delete=models.CASCADE, related_name='reservation_messages')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['updated_at',]

# Message Model used for UserMemo Chat

class UserMemoMessage(models.Model):
    usermemo = models.ForeignKey(UserMemo,on_delete=models.CASCADE,related_name="memo_messages")
    sender = models.ForeignKey(User,on_delete=models.CASCADE, related_name='memo_sender_message')
    title = models.CharField(max_length=200)
    message = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['updated_at',]

# Message Model used for Template Reservation Message. Currently we are saving the data but not listing anywhere. No proper logic provided from japan team.

class TemplateReservationMessage(models.Model):
    template = models.ForeignKey(Template,on_delete=models.CASCADE, related_name='template_message',null=True,blank=True)
    reservation_message = models.ForeignKey(ReservationMessage,on_delete=models.CASCADE, related_name='message_template',null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['updated_at',]