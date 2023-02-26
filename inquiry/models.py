from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from drugstore.models import DrugStore
from inquiry.tasks import send_email_when_notice_inquiry_created,send_email_when_notice_inquiry_resolved
from django.utils.translation import gettext as _
from pharmacy_auth.models import User
from django.core.mail import send_mail
# Create your models here.

# Inquiry Categories

class InquiryCategoryChoices(models.TextChoices):
	ABOUT_MY_CLINIC = ('About my clinic','About my clinic')
	ABOUT_MY_CLINIC_JPN = ('じぶん薬局について','じぶん薬局について')
	HOW_TO_USE_THE_SITE_OR_SERVICES = ('How to use the site/services','How to use the site/services')
	HOW_TO_USE_THE_SITE_OR_SERVICES_JPN = ('ADARSHサイト・サービスの利用方法','サイト・サービスの利用方法')
	INQUIRIES_REGARDING_REGISTRATION_AND_LOGIN = ('Inquiries regarding registration and login','Inquiries regarding registration and login')
	INQUIRIES_REGARDING_REGISTRATION_AND_LOGIN_JPN = ('登録やログインに関するお問いわせ','登録やログインに関するお問いわせ')
	INQUIRIES_REGARDING_PASSWORD = ('Inquiries regarding Password Reset','Inquiries regarding Password Reset')
	INQUIRIES_REGARDING_PASSWORD_JPN = ('パスワードリセットに関するお問い合わせ','パスワードリセットに関するお問い合わせ')
	OTHER_INQUIRIES = ('Other inquiries','Other inquiries')
	OTHER_INQUIRIES_JPN = ('その他のお問い合わせ','その他のお問い合わせ')

# Inquiry Model for noting all the user inquiries and queries

class Inquiry(models.Model):
	contact_category = models.CharField(max_length=50, choices=InquiryCategoryChoices.choices, default=InquiryCategoryChoices.OTHER_INQUIRIES)
	name = models.CharField(max_length=20)
	email = models.EmailField('email address')
	inquiry_user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name="user_inquiries")
	inquiry_pharmacy =models.ForeignKey(DrugStore,on_delete=models.CASCADE,null=True,blank=True,related_name="pharmacy_inquiries")
	contents_of_inquiry = models.TextField(max_length=100)
	is_resolved = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-updated_at',]

class InquiryMessage(models.Model):
	inquiry= models.ForeignKey(Inquiry,on_delete=models.CASCADE,null=True,blank=True,related_name="inquiry_messages")
	message = models.TextField(max_length=100)
	sender = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-updated_at',]

@receiver(post_save, sender=Inquiry)
def send_inquiry_email(sender,created,instance, **kwargs):
	if created:
		# send_email_when_notice_inquiry_created([instance.pk], countdown=10)
		send_email_when_notice_inquiry_created(instance.pk)
		if instance.email:
			user_objs = User.objects.filter(email=instance.email)
			if user_objs.count():
				user_obj = user_objs.first()
				if user_obj.is_patient:
					if((instance.contact_category=="Inquiries regarding Password Reset") or (instance.contact_category=="パスワードリセットに関するお問い合わせ")) :
						send_mail(
							'パスワードの再設定を受付けました',
							"じぶん薬局における、ご利用パスワードの再設定を受付けました。\n以下のリンクをクリックorタップいただくと、パスワード再設定画面に移動します。\nそちらからパスワードの再設定を完了してください。\n{}\nこのメールに心当たりのない方は、お手数ですが本メールを破棄してください。\nまた、本メールに関するお問い合わせは運営事務局までお願いいたします。\n\n////////////\nじぶん薬局運営事務局\n住所：〒254-0014\n神奈川県平塚市四之宮1-4-13\nE-mail：info@orthros.com".format("https://pharmacy-user.netlify.app/password"),
							'developers.geitpl@gmail.com',
							[instance.email,'karre@eoraa.com'],
						)
				elif user_obj.is_pharmacy:
					send_mail(
						'{} 様よりメッセージが届いています'.format(instance.name),
						'{} 様 \n\n {} 様からメッセージが届いています。お手数ですが、以下のURLからサイトにアクセスいただき、メッセージを確認していただけますようよろしくお願いいたします。\n {} \n\n////////////\nじぶん薬局運営事務局\n 住所：〒254-0014\n神奈川県平塚市四之宮1-4-13 \nE-mail：info@orthros.com'.format(instance.inquiry_pharmacy.drugstore_name,instance.name,'https://pharma-company.netlify.app/'),
						'developers.geitpl@gmail.com',
						[instance.inquiry_pharmacy.email,'karre@eoraa.com'],
					)		

				admin_list = [u.email for u in User.objects.filter(is_superuser=True)]
				admin_list.append('karre@eoraa.com')
				send_mail(
					'{} 様よりメッセージが届いています'.format(instance.name),
					'{} 様からメッセージが届いています。\n以下のURLからメッセージを確認してください。\n\n{}'.format(instance.name,'https://dev-pharma-cms.eoraa.com/'),
					'developers.geitpl@gmail.com',
					admin_list,
				)		

				InquiryMessage.objects.create(inquiry=instance,sender=user_obj,message=instance.contents_of_inquiry)
		
@receiver(post_save, sender=InquiryMessage)
def inquiry_update(sender,created,instance, **kwargs):
	if instance.inquiry.is_resolved:
		send_email_when_notice_inquiry_resolved(instance.id)
