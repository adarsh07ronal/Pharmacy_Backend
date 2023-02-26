from django.db import models
from patient.models import Patient, Prescription
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from drugstore.models import DrugStore
from django.core.mail import send_mail

User = get_user_model()

# Create your models here.
# For creating reservation for an appointement
class Recieve_choice(models.Model):
    choice_en=models.CharField(max_length=200,null=True,blank=True) 
    choice_jpn=models.CharField(max_length=200,null=True,blank=True)

class ForReservation(models.Model):
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE, related_name='patient_for_reservation')
    prescription = models.ManyToManyField(Prescription,null=True,blank=True, related_name='reservations')
    pharmacy = models.ForeignKey(DrugStore,on_delete=models.CASCADE, related_name='user_for_reservation')
    is_visted = models.BooleanField(blank=True,null=True,default=False)
    is_accepted = models.BooleanField(blank=True,null=True,default=False)
    is_remote_accepted = models.BooleanField(blank=True,null=True,default=False)
    medication_guidence = models.BooleanField(blank=True,null=True,default=False)
    remote_medication = models.CharField(max_length=200,null=True,blank=True)
    scheduled_by =models.ForeignKey(User,blank=True,null=True,related_name="reservation_scheduler",on_delete=models.CASCADE)
    # send_from = models.CharField(max_length=15,choices=(("from user","from user"),("from pharmacy","from pharmacy")),blank=True,null=True)
    message = models.TextField(null=True,blank=True)
    is_seen_patient = models.BooleanField(default=True)
    is_seen_pharmacy = models.BooleanField(default=True)
    reservation_scheduled_time = models.DateTimeField(blank=True,null=True)
    remote_medication_scheduled_by=models.ForeignKey(User,blank=True,null=True,related_name="guidance_scheduler",on_delete=models.CASCADE)
    guidance_scheduled_time = models.DateTimeField(blank=True,null=True)
    receive_prescription_by = models.ForeignKey(Recieve_choice,null=True,blank=True,on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at',]

class UserMemo(models.Model):
    pharmacy_name = models.CharField(max_length=100,null=True,blank=True)
    pharmacist = models.CharField(max_length=100,null=True,blank=True)
    pharmacy = models.ForeignKey(DrugStore,on_delete=models.CASCADE,null=True,blank=True)
    prescription_reservation = models.ForeignKey(ForReservation,null=True,blank=True,on_delete=models.CASCADE, related_name='reservation_memos')
    prescription = models.ManyToManyField(Prescription,null=True,blank=True, related_name='memos')
    title = models.CharField(max_length=200,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    user = models.ForeignKey(User,blank=False,related_name="memo_user",on_delete=models.CASCADE)
    memo_scheduled_time = models.DateField(null=True,blank=True)
    is_usermemo_added = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at',]

@receiver(post_save, sender=ForReservation)
def reservation_save(sender, instance,created,*args, **kwargs):
    if created:
        if instance.reservation_scheduled_time:
            reservation_date =str(instance.reservation_scheduled_time)
            l=reservation_date.split("-")
            ll =l[2].split(" ")
            reservation_date=l[0]+"年"+l[1]+"月"+ll[0]+"日 "+ll[1][0:5]
            send_mail(
                '処方箋受取の予約申請をおこないました',
                "{} 様\n\n処方箋受取予約申請をおこないました。\n以下の日程となりますので、お忘れのないようにお受け取りください。\n\n日程\n{}\n\nなお、申請いただいた日程は、確定ではありません。\n{} にて確認の上、承諾があり次第確定となります。\n申請いただいた日程での受取ができない場合、修正依頼が届きますので、\nお手数ですが再設定をお願いいたします。\n\n////////////\nじぶん薬局運営事務局\n\n住所：〒254-0014\n神奈川県平塚市四之宮1-4-13\nE-mail：info@orthros.com".format(instance.patient.name,reservation_date,instance.pharmacy.drugstore_name),
                'developers.geitpl@gmail.com',
                [instance.patient.email,'karre@eoraa.com'],
            )		
        send_mail(
            '処方箋受取の予約申請が届きました',
            "{} 様\n\n{} 様より、処方箋受取の予約申請が届きました。\n予約管理画面より予約をご確認いただき、承認または修正手続きを\n行っていただけますよう、よろしくお願いいたします。\n{}\n\n////////////\nじぶん薬局運営事務局\n住所：〒254-0014\n神奈川県平塚市四之宮1-4-13\nE-mail：info@orthros.com".format(instance.pharmacy.representative,instance.patient.name,'https://pharma-company.netlify.app/mypage'),
            'developers.geitpl@gmail.com',
            [instance.pharmacy.email,'karre@eoraa.com'],
        )	
        if instance.medication_guidence:
            send_mail(
                '遠隔服薬指導の予約申請が届きました',
                "{} 様\n\n{} 様より、遠隔服薬指導の予約申請が届きました。\n予約管理画面より予約をご確認いただき、承認または修正手続きを\n行っていただけますよう、よろしくお願いいたします。\n{}\n\n////////////\nじぶん薬局運営事務局\n住所：〒254-0014\n神奈川県平塚市四之宮1-4-13\nE-mail：info@orthros.com".format(instance.pharmacy.representative,instance.patient.name,'https://pharma-company.netlify.app/mypage'),
                'developers.geitpl@gmail.com',
                [instance.pharmacy.email,'karre@eoraa.com'],
            )
            if instance.guidance_scheduled_time:
                guidance_date =str(instance.guidance_scheduled_time)
                l=guidance_date.split("-")
                ll =l[2].split(" ")
                guidance_date=l[0]+"年"+l[1]+"月"+ll[0]+"日 "+ll[1][0:5]
                send_mail(
                    '遠隔服薬指導の予約申請をおこないました',
                    "{} 様\n\n遠隔服薬指導の予約申請をおこないました。\n以下の日程となりますので、お忘れのないようにお願いいたします。\n\n日程\n{}\n\nなお、申請いただいた日程は、確定ではありません。\n{} にて確認の上、承諾があり次第確定となります。\n申請いただいた日程での実施ができない場合、修正依頼が届きますので、\nお手数ですが再設定をお願いいたします。\n\n////////////\nじぶん薬局運営事務局\n住所：〒254-0014\n神奈川県平塚市四之宮1-4-13\nE-mail：info@orthros.com".format(instance.patient.name,guidance_date,instance.pharmacy.drugstore_name),
                    'developers.geitpl@gmail.com',
                    [instance.patient.email,'karre@eoraa.com'],
                )
    
#if reservation got accepted ,we will  fill that details in reservation model 
class Reservation(models.Model):
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE, related_name='patient_reservation')
    prescription = models.ForeignKey(Prescription,on_delete=models.CASCADE, related_name='presciption_reservation')
    scheduled_time = models.DateTimeField(blank=True,null=True)
    pharmacy = models.ForeignKey(User,on_delete=models.CASCADE, related_name='user_reservation')
    is_remote = models.BooleanField(default=False)
    message = models.TextField()