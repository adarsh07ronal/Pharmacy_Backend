from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
# Create your models here.
import threading
from django.http import HttpResponse

from django.core.mail import (BadHeaderError)


class NotificeStatusChoices(models.Model):
    status_choice = models.IntegerField(null=True,blank=True)
    status_en = models.CharField(max_length=50,null=True,blank=True)
    status_jpn = models.CharField(max_length=50,null=True,blank=True)

class NotificeDeliveryChoices(models.Model):
    delivery_target_choice = models.IntegerField(null=True,blank=True)
    delivery_target_en = models.CharField(max_length=50,null=True,blank=True)
    delivery_target_jpn = models.CharField(max_length=50,null=True,blank=True)

def default_status():
    s_obj =NotificeStatusChoices.objects.all()
    if s_obj.count():
        return s_obj[0].id
    else:
        return None

def default_delivery():
    d_obj =NotificeDeliveryChoices.objects.all()
    if d_obj.count():
        return d_obj[0].id
    else:
        return None

# Notice Model to store notification(CMS) information 

class Notice(models.Model):
	title = models.CharField(max_length=200,null=True,blank=True)
	text = models.TextField(null=True,blank=True)
	#status = models.ForeignKey(NotificeStatusChoices,on_delete=models.DO_NOTHING,null=True,blank=True)
	status = models.ForeignKey(NotificeStatusChoices,on_delete=models.DO_NOTHING,default=default_status,null=True,blank=True)
	image_registration=models.ImageField(upload_to='notice/registration',null=True,blank=True)
	date = models.DateField(null=True,blank=True)
	#delivery_target = models.ForeignKey(NotificeDeliveryChoices,on_delete=models.DO_NOTHING,null=True,blank=True)
	delivery_target = models.ForeignKey(NotificeDeliveryChoices,on_delete=models.DO_NOTHING,default=default_delivery)
	deliver_start_time = models.DateField(null=True,blank=True)
	deliver_end_time = models.DateField(null=True,blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = "Notice"
		verbose_name_plural = "Notices"
		ordering = ('-updated_at',)   

# BroadCasting the emails whenever the notification is created from CMS

class EmailThread(threading.Thread):
    def __init__(self, instance_list):
        self.instance_list = instance_list
        # self.delivery_type = delivery_type
        threading.Thread.__init__(self)

    def run(self):
        for instance in self.instance_list:
            html_message = render_to_string('notice/notice_info.html', {'instance':instance})
            msg = EmailMultiAlternatives("じぶん薬局の会員登録完了",html_message , instance.email, [instance.email,'karre@eoraa.com'])
            msg.attach_alternative(html_message, "text/html")
            try:
                msg.send()
            except BadHeaderError:
                return HttpResponse('Invalid header found.')

@receiver(post_save, sender=Notice)
def send_notice_email(sender,created,instance, **kwargs):
    if created:
        from pharmacy_auth.models import User
        s_m = 0
        if instance.delivery_target.delivery_target_choice == 1:
            list_user = [ u for u in User.objects.filter(is_superuser=False) ]
            s_m = 1
        if instance.delivery_target.delivery_target_choice == 3:
            list_user = [ u for u in User.objects.filter(is_patient=True) ]
            s_m = 1
        if instance.delivery_target.delivery_target_choice == 4:            
            list_user = [ u for u in User.objects.filter(is_pharmacy=True) ]
            s_m = 1
        if s_m ==1:
            list_user.append(User.objects.get(email="karre@eoraa.com"))
            EmailThread(list_user).start()