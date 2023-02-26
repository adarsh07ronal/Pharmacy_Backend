from django.db import models
from django.conf import settings

# Currently Not using any of the below models. This was previously setup by Yogesh

class Notification(models.Model):
    title = models.CharField(max_length=50)
    message = models.TextField()
    date_time = models.DateTimeField(auto_now=True)
    status_choice = (
        ("Unread","Unread"),
        ("Read","Read"),
    )
    status = models.CharField(max_length=8, choices=status_choice,default="Unread")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name='notifications')
    date_read = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = "notifications"
        verbose_name_plural = "notifications"

class EmailNotification(models.Model):
    Slug =  models.SlugField(unique=True)
    slug_details = models.TextField(max_length=500,help_text="Detailed description of email when it send")
    subject = models.CharField(max_length=200)
    body = models.TextField()
    delivery_choice = (
        ('Immediate','Immediate'),
        ('Scheduled','Scheduled'),
    )
    delivery_type = models.CharField(max_length=9,choices=delivery_choice)
    deliver_time = models.TimeField(help_text="required if scheduled selected")
    record_log = models.BooleanField(default=False)
    pharmacy = models.BooleanField(default=False)
    patient = models.BooleanField(default=False)
    orthrus = models.BooleanField(default=False)
    updated_at =  models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at',]