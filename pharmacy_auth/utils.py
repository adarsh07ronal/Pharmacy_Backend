from random import randrange
from django.core.mail import send_mail
from pharmacy_auth.models import Otp


def otp_create(user):
	otp = randrange(10000, 1000000)
	otp_obj = Otp.objects.create(user=user, otp=otp)
	return otp_obj

def user_send_mail(user, otp):
	send_mail("OTP varification", "Your otp is {}".format(otp.otp), 'developers.geitpl@gmail.com', [user.email])
	return True