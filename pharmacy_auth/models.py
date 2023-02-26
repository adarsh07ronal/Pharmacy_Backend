from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email=email, password=password, **extra_fields)

class AdministratorStatus(models.Model):
    status_id = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        if self.status_id and self.status:
            return str(self.status)
        return str(self.id)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username= models.CharField(null=True,blank=True,max_length=100)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_pharmacy = models.BooleanField(max_length=10, default=False)
    is_patient = models.BooleanField(default=False)
    is_editor = models.BooleanField(default=False)
    is_viewer = models.BooleanField(default=False)
    is_administrator = models.BooleanField(default=False)
    is_orthrus = models.BooleanField(default=False)
    is_email_verified =models.BooleanField(default=False)
    is_verification_updated =models.BooleanField(default=False)
    is_import_creation=models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    # Return something meaningful
    def __str__(self):
        return '{}'.format(self.email)

    @property
    def status(self):
        if self.is_active:
            return 'Active'
        else:
            return 'Inactive'

    class Meta:
        unique_together = ['email']
        ordering =['-updated_at']

@receiver(post_save, sender=User)
def send_inquiry_email(sender,created,instance, **kwargs):
    if created:
        from patient.models import Patient
        from drugstore.models import DrugStore
        if instance.username is None:
            instance.username =instance.email
            # .split("@")[0]
        if instance.is_patient:
            if not instance.is_import_creation:
                send_mail(
                    'じぶん薬局の会員登録認証',
                    "じぶん薬局運営事務局です。\nこの度は、会員登録申請をありがとうございます。\n以下の認証URLをクリックorタップして、本登録へ進んでください。\n\nhttps://dev-pharmacy.eoraa.com/api/email/verification/?id={}\nこのメールに心当たりのない方は、お手数ですが本メールを破棄してください。\nまた、本メールに関するお問い合わせは運営事務局までお願いいたします。\n\n////////////\nじぶん薬局運営事務局\n住所：〒254-0014\n神奈川県平塚市四之宮1-4-13\nE-mail：info@orthros.com".format(instance.id),
                    'developers.geitpl@gmail.com',
                    [instance.email,'karre@eoraa.com'],
                )
                patient_objs = Patient.objects.filter(email=instance.email)
                if patient_objs.count():
                    patient_obj = patient_objs.first()
                    # if patient_obj.user is None:
                    patient_obj.user=instance
                    patient_obj.save()
                else:
                    # if instance.username:
                        # Patient.objects.create(user=instance,name=instance.username,email=instance.email)
                    # else:
                    Patient.objects.create(user=instance,name=instance.email,email=instance.email)
        if instance.is_pharmacy:
            drugstore_objs = DrugStore.objects.filter(email=instance.email)
            if drugstore_objs.count():
                drugstore_obj = drugstore_objs.first()
                drugstore_obj.user=instance
                drugstore_obj.save() 
        if instance.is_superuser:
            admin_list = [u.email for u in User.objects.filter(is_superuser=True,is_administrator=True)]
            admin_list.append('karre@eoraa.com')
            send_mail(
				'新規会員登録が発生しました',
                "新規会員登録が発生しました。\n詳細なユーザー情報は以下のURLから確認ください。\n{}".format("https://dev-pharma-cms.eoraa.com/adminInfo/"),
                'developers.geitpl@gmail.com',
                admin_list,
			)
            
    if instance.is_verification_updated==True:
        instance.is_verification_updated=False
        sm=0
        if instance.is_patient:
            login_url = "https://pharmacy-user.netlify.app/"
            sm=1
        if instance.is_pharmacy:
            login_url = "https://pharma-company.netlify.app/"
            sm=1
        
        if sm==1:
            send_mail(
                'じぶん薬局の会員登録完了',
                "じぶん薬局運営事務局です。\n会員登録は正常に完了しました。\n以下のアドレスからマイページにアクセスいただき、\nご登録いただいたメールアドレスとパスワードでログインしてください。\n{}\n\nマイページの情報を正しくご登録いただければ、より便利にサービスをご利用いただくことができます。\n\n////////////\nじぶん薬局運営事務局\n住所：〒254-0014\n神奈川県平塚市四之宮1-4-13\nE-mail：info@orthros.com".format(login_url),
                'developers.geitpl@gmail.com',
                [instance.email,'karre@eoraa.com'],
            )
        instance.save()

class Otp(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_otp')
    otp = models.CharField(max_length=9, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
