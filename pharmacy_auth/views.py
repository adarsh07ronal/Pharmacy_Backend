from django.utils import timezone
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from patient.models import Patient
from pharmaceutical_manufacturer.serializers import AdvertisementDashboardSerializer
from pharmacy_auth.serializers import UserPatientSerializer, UserOrthrusSerializer, UserPharmacySerializer, RegisteredUserSerializer, UserSerializer, ChangePasswordSerializer,AdministratorStatusSerializer,UserManagementSerializer, CMSUserSerializer,CMSUserCreateSerializer, RegisteredPharmacySerializer
from pharmacy_auth.models import AdministratorStatus, User
# from pharmacy_auth.utils import otp_create, user_send_mail
from patient.serializers import PatientInformationUserManagementSerializer
from drugstore.serializers import DrugStoreSerializer
from django.core.mail import send_mail
from pharmacy.permissions import IsCMS
from pharmaceutical_manufacturer.models import *
from inquiry.models import Inquiry
from inquiry.serializers import InquiryPatientSerializer,InquiryPharmacySerializer
from django.http import HttpResponseRedirect
import json
from rest_framework.renderers import TemplateHTMLRenderer
from django.shortcuts import render
import requests

class PatientSignupViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserPatientSerializer
	http_method_names=['post']

	def create(self, request,*args,**kwargs):
		try:
			email = request.data.get('email')
			password= request.data.get("password")
			special_characters = """!@#$%^&*()-+?_=,<>/"""
			if email==None or email=="":
				return Response({'email':'メールアドレスは必須です'}, status=status.HTTP_400_BAD_REQUEST)
			if password==None or password=="":
				return Response({'password':'ログインパスワードは必須です'}, status=status.HTTP_400_BAD_REQUEST)
			if User.objects.filter(email=email):
					return Response({'email':'このログインIDはすでに登録されています。ログインをお試しください'}, status=status.HTTP_400_BAD_REQUEST)
			serializer=UserSerializer(data=request.data)
			if serializer.is_valid():
				if any(i in special_characters for i in password) and any(char.isalpha() for char in password) and any(char.isdigit() for char in password):
					user = User.objects.create(email=email,is_patient=True)
					user.set_password(password)
					user.save()
					user_token, created = Token.objects.get_or_create(user=user)
					return Response(UserSerializer(user).data)
				else:
					return Response({"password":"パスワードは半角英数でご入力ください"}, status=status.HTTP_400_BAD_REQUEST)
			else:
				return Response({"email":"メールアドレスの形式に誤りがあります"}, status=status.HTTP_400_BAD_REQUEST)
		except Exception as e:
			return Response({"message":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class OrthrusSignupViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserOrthrusSerializer
	http_method_names = ['post']

	def create(self, request):
		special_characters = """!@#$%^&*()-+?_=,<>/"""
		email = request.data.get('email')
		password= request.data.get("password")
		if email==None or email=="":
			return Response({'email':'メールアドレスは必須です'}, status=status.HTTP_400_BAD_REQUEST)
		if password==None or password=="":
			return Response({'password':'ログインパスワードは必須です'}, status=status.HTTP_400_BAD_REQUEST)
		if User.objects.filter(email=email):
				return Response({'email':'このログインIDはすでに登録されています。ログインをお試しください'}, status=status.HTTP_400_BAD_REQUEST)
		serializer=UserSerializer(data=request.data)
		if serializer.is_valid():
			if any(i in special_characters for i in password) and any(char.isalpha() for char in password) and any(char.isdigit() for char in password):
				user = User.objects.create(email=email)
				user.set_password(password)
				user.is_orthrus=True
				user.save()
				user_token, created = Token.objects.get_or_create(user=user)
				return Response(UserSerializer(user).data)
			else:
				return Response({"password":"パスワードは半角英数でご入力ください"}, status=status.HTTP_400_BAD_REQUEST)
		else:
			return Response({"email":"メールアドレスの形式に誤りがあります"}, status=status.HTTP_400_BAD_REQUEST)

class OrthrusUserManagementApiView(APIView):
	
	"""
	CRUD User Management

	Request Data : {
		"username" : "",
		"email": "",
		"administrator_status":1,
		"password": ""
	}
	"""

	permission_classes = [IsCMS]

	def get(self,request,*args,**kwargs):
		try:
			instances = User.objects.filter(is_superuser=True)
			if instances.count():
				return Response(data=UserManagementSerializer(instances,many=True).data,status=status.HTTP_200_OK)
			return Response({"message":"ユーザーのデータが見つかりません"},status=status.HTTP_404_NOT_FOUND)
		except Exception as e:
			return Response({"message":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
	
	def post(self, request,*args,**kwargs):
		special_characters = """!@#$%^&*()-+?_=,<>/"""
		email = request.data.get('email')
		administrator_status = request.data.get('administrator_status')
		password= request.data.get("password")
		if email==None or email=="":
			return Response({'email':'メールアドレスは必須です'}, status=status.HTTP_400_BAD_REQUEST)
		if password==None or password=="":
			return Response({'password':'ログインパスワードは必須です'}, status=status.HTTP_400_BAD_REQUEST)
		if User.objects.filter(email=email):
				return Response({'email':'このログインIDはすでに登録されています。ログインをお試しください'}, status=status.HTTP_400_BAD_REQUEST)
		serializer=UserManagementSerializer(data=request.data)
		if serializer.is_valid():
			if any(i in special_characters for i in password) and any(char.isalpha() for char in password) and any(char.isdigit() for char in password):
				user = User.objects.create(email=email,username=request.data["username"],is_orthrus=True,is_superuser = True)
				user.set_password(password)
				if administrator_status == 1:
					user.is_administrator = True
				elif administrator_status == 2:
					user.is_editor = True
				elif administrator_status == 3:
					user.is_viewer = True
				user.is_email_verified=True
				user.save()
				user_token, created = Token.objects.get_or_create(user=user)
				login_url = "https://dev-pharma-cms.eoraa.com/"
				send_mail(
					'じぶん薬局の会員登録完了',
					"じぶん薬局運営事務局です。\n会員登録は正常に完了しました。\n以下のアドレスからマイページにアクセスいただき、\nログイン情報\nメールアドレス：{}\nパスワード：{}\nご登録いただいたメールアドレスとパスワードでログインしてください。\n{}\n\nマイページの情報を正しくご登録いただければ、より便利にサービスをご利用いただくことができます。\n\n////////////\nじぶん薬局運営事務局\n住所：〒254-0014\n神奈川県平塚市四之宮1-4-13\nE-mail：info@orthros.com".format(email,password,login_url),
					'developers.geitpl@gmail.com',
					[email,'karre@eoraa.com'],
				)
				return Response(UserManagementSerializer(user).data)
			else:
				return Response({"password":"パスワードは半角英数でご入力ください"}, status=status.HTTP_400_BAD_REQUEST)
		else:
			return Response({"email":"メールアドレスの形式に誤りがあります"}, status=status.HTTP_400_BAD_REQUEST)

class RegisteredUserManagement(APIView):
	
	"""
	Registered User Management

	Params :
	{
		"patient_id" : 4441
	}

	"""

	permission_classes = [IsCMS]

	def get(self,request,*args,**kwargs):
		try:
			if "patient_id" in self.request.GET:
				patient_instances = Patient.objects.filter(id=self.request.GET["patient_id"])
				if patient_instances.count():
					patient_instance =patient_instances.first()
					instance = patient_instance.user
					return Response(data=RegisteredUserSerializer(instance).data,status=status.HTTP_200_OK)
			else:
				data = {}
				instances =Patient.objects.all()
				data["patient"] = PatientInformationUserManagementSerializer(instances,many=True).data
				return Response(data=data,status=status.HTTP_200_OK)
			return Response({"message":"ユーザーのデータが見つかりません"},status=status.HTTP_404_NOT_FOUND)
		except Exception as e:
			return Response({"message":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RegisteredPharmacyManagement(APIView):
	
	"""
	Registered Pharmacy Management

	Params :
	{
		"pharmacy_id" : 48
	}

	"""

	permission_classes = [IsCMS]

	def get(self,request,*args,**kwargs):
		try:
			from drugstore.models import DrugStore
			if "pharmacy_id" in self.request.GET:
				pharmacy_instances = DrugStore.objects.filter(id=self.request.GET["pharmacy_id"])
				if pharmacy_instances.count():
					pharmacy_instance =pharmacy_instances.first()
					# instance = pharmacy_instance.user						
					return Response(data=RegisteredPharmacySerializer(pharmacy_instance).data,status=status.HTTP_200_OK)
			else:
				instances = DrugStore.objects.all()
				return Response(data=DrugStoreSerializer(instances,many=True).data,status=status.HTTP_200_OK)
			return Response({"message":"ユーザーのデータが見つかりません"},status=status.HTTP_404_NOT_FOUND)
		except Exception as e:
			return Response({"message":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class OrthrusUserManagementRetrieveUpdateDeleteAPIView(APIView):
		
	"""
	CRUD User Management

	Request Data : {
		"username" : "",
		"email": "",
		"administrator_status":1,
		"password": ""
	}
	"""
	permission_classes = [IsCMS]

	def get(self,request,*args,**kwargs):
		pk = self.kwargs["id"]
		queryset = User.objects.filter(id=pk)
		if queryset.count():
			queryset = queryset.first()
			serializer=UserManagementSerializer(queryset)
			return Response(data=serializer.data, status=status.HTTP_200_OK)
		return Response({"message":"ユーザーデータが見つかりません"}, status=status.HTTP_404_NOT_FOUND)

	def put(self,request,*args,**kwargs):
		pk = self.kwargs["id"]
		instance = User.objects.filter(id=pk)
		if instance.count():
			instance = instance.first()
			special_characters = """!@#$%^&*()-+?_=,<>/"""
			if "email" in request.data:
				email = request.data.get('email')
				if User.objects.filter(email=email).exclude(id=instance.id):
						return Response({'email':'このログインIDはすでに登録されています。ログインをお試しください'}, status=status.HTTP_400_BAD_REQUEST)
			serializer=UserManagementSerializer(instance,data=request.data,partial=True)
			if serializer.is_valid():
				serializer.save()
				if "password" in request.data:
					password= request.data.get("password")
					if any(i in special_characters for i in password) and any(char.isalpha() for char in password) and any(char.isdigit() for char in password):
						instance.set_password(password)
					else:
						return Response({"password":"パスワードは半角英数でご入力ください"}, status=status.HTTP_400_BAD_REQUEST)
				if "administrator_status" in request.data:
					administrator_status = request.data.get('administrator_status')
					instance.is_administrator = False
					instance.is_editor = False
					instance.is_viewer = False
					if administrator_status == 1:
						instance.is_administrator = True
					elif administrator_status == 2:
						instance.is_editor = True
					elif administrator_status == 3:
						instance.is_viewer = True
				instance.save()
				user_token, created = Token.objects.get_or_create(user=instance)
				return Response(UserManagementSerializer(instance).data)
			else:
				return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		else:
			return Response({"message":"ユーザーのデータが見つかりません"},status=status.HTTP_404_NOT_FOUND)

	def delete(self, request,*args,**kwargs):
		try:
			pk = self.kwargs["id"]
			instance = User.objects.filter(id=pk)
			if instance.count():
				instance.delete()
				return Response(status=status.HTTP_204_NO_CONTENT)    
			else:
				return Response({"message":"ユーザーのデータが見つかりません"},status=status.HTTP_404_NOT_FOUND)
		except Exception as e:
			return Response({"message":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CMSUserUpdateAPIView(APIView):
		
	"""
	CRUD CMS Update User

	Request Data : {
		"username" : "",
		"email": "",
		"password": ""
	}
	"""

	def put(self,request,*args,**kwargs):
		pk = self.kwargs["id"]
		instance = User.objects.filter(id=pk)
		if instance.count():
			instance = instance.first()
			special_characters = """!@#$%^&*()-+?_=,<>/"""
			if "email" in request.data:
				email = request.data.get('email')
				if User.objects.filter(email=email).exclude(id=instance.id):
						return Response({'email':'このログインIDはすでに登録されています。ログインをお試しください'}, status=status.HTTP_400_BAD_REQUEST)
			serializer=CMSUserCreateSerializer(instance,data=request.data,partial=True)
			if serializer.is_valid():
				serializer.save()
				if "password" in request.data:
					password= request.data.get("password")
					if any(i in special_characters for i in password) and any(char.isalpha() for char in password) and any(char.isdigit() for char in password):
						instance.set_password(password)
					else:
						return Response({"password":"パスワードは半角英数でご入力ください"}, status=status.HTTP_400_BAD_REQUEST)
				instance.save()
				user_token, created = Token.objects.get_or_create(user=instance)
				return Response(CMSUserSerializer(instance).data)
			else:
				return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		else:
			return Response({"message":"ユーザーのデータが見つかりません"},status=status.HTTP_404_NOT_FOUND)

class PharmacySignupViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserPharmacySerializer
	http_method_names = ['post']

	def create(self, request):
		special_characters = """!@#$%^&*()-+?_=,<>/"""
		email = request.data.get('email')
		password= request.data.get("password")
		if email==None or email=="":
			return Response({'email':'メールアドレスは必須です.'}, status=status.HTTP_400_BAD_REQUEST)
		if password==None or password=="":
			return Response({'password':'ログインパスワードは必須です.'}, status=status.HTTP_400_BAD_REQUEST)
		if User.objects.filter(email=email):
				return Response({'email':'このログインIDはすでに登録されています。ログインをお試しください.'}, status=status.HTTP_400_BAD_REQUEST)
		serializer=UserSerializer(data=request.data)
		if serializer.is_valid():
			if any(i in special_characters for i in password) and any(char.isalpha() for char in password) and any(char.isdigit() for char in password):
				user = User.objects.create(email=email)
				user.set_password(password)
				user.is_pharmacy=True
				user.save()
				user_token, created = Token.objects.get_or_create(user=user)
				return Response(UserSerializer(user).data)
			else:
				return Response({"password":"パスワードは半角英数でご入力ください."}, status=status.HTTP_400_BAD_REQUEST)
		else:
			return Response({"email":"メールアドレスの形式に誤りがあります."}, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordOtpApi(APIView):
	@swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING,
                                           description='email'),
            },
            required=['email'],
        ),
        responses={status.HTTP_200_OK:UserSerializer}
    )
	def post(self, request):
		email = request.data.get('email')
		try:
			user = User.objects.get(email=email)
		except:
			return Response({'email':"正しいメールアドレスを入力してください."}, status=status.HTTP_400_BAD_REQUEST)
		send_mail(
						'パスワードの再設定を受付けました',
						"じぶん薬局における、ご利用パスワードの再設定を受付けました。\n以下のリンクをクリックorタップいただくと、パスワード再設定画面に移動します。\nそちらからパスワードの再設定を完了してください。\n{}\nこのメールに心当たりのない方は、お手数ですが本メールを破棄してください。\nまた、本メールに関するお問い合わせは運営事務局までお願いいたします。\n\n////////////\nじぶん薬局運営事務局\n住所：〒254-0014\n神奈川県平塚市四之宮1-4-13\nE-mail：info@orthros.com".format('https://pharmacy-user.netlify.app/newPassword?email={}'.format(email)),
						'developers.geitpl@gmail.com',
						[user.email,'karre@eoraa.com'],
		)
		return Response({"message":"確認メールが送信されました."})


class VerifyOtpApi(APIView):
	@swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING,
                                           description='email'),
                'otp': openapi.Schema(type=openapi.TYPE_STRING, description='otp')
            },
            required=['email', 'otp'],
        ),
        responses={status.HTTP_200_OK:UserSerializer}
    )

	def post(self, request):
		email = request.data.get('email')
		try:
			user = User.objects.get(email=email)
		except:
			return Response({'email':"正しいメールアドレスを入力してください."}, status=status.HTTP_400_BAD_REQUEST)
		otp=request.data.get('otp')
		created_at=timezone.now()-timezone.timedelta(seconds=10*60)
		try:
			otp_obj=user.user_otp.get(otp=otp,created_at__lte=timezone.now(),created_at__gte=created_at,is_active=True)
		except:
			return Response({"Otp":"無効なワンタイムパスワードです。再度お試しください"}, status=status.HTTP_400_BAD_REQUEST)
		otp_obj.is_active=False
		otp_obj.save()
		return Response({ "message":"ワンタイムパスワードが正常に一致しました.","user":UserSerializer(user).data})


class ResetPasswordApi(APIView):
	@swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING,
                                           description='email'),
                'password': openapi.Schema(type=openapi.TYPE_STRING,
                                          description='password'),
                'confirm_password': openapi.Schema(type=openapi.TYPE_STRING, description='old password'),
            },
            required=['email', 'password','confirm_password'],
        ),
        responses={status.HTTP_200_OK:UserSerializer}
    )

	def post(self, request):
		special_characters = """!@#$%^&*()-+?_=,<>/"""
		email = request.data.get('email')
		try:
			user = User.objects.get(email=email)
		except:
			return Response({"email": "正しいメールアドレスを入力してください."}, status=status.HTTP_400_BAD_REQUEST)
		password = request.data.get('password')
		if any(i in special_characters for i in password) and any(char.isalpha() for char in password) and any(char.isdigit() for char in password):
			confirm_password = request.data.get('confirm_password')
			if password==confirm_password:
				user.set_password(password)
				user.save()
				return Response({ "password":"パスワードのリセットが完了しました.","user":UserSerializer(user).data})
			else:
				return Response({'password': "パスワードが一致しません."}, status=status.HTTP_400_BAD_REQUEST)
		else:
			return Response({"password":"パスワードは半角英数でご入力ください."}, status=status.HTTP_400_BAD_REQUEST) 

class ChangePasswordApi(generics.UpdateAPIView):
	serializer_class = ChangePasswordSerializer
	permission_classes=[IsAuthenticated]
	#authentication_classes = (TokenAuthentication, )
	model = User

	def get_object(self, queryset=None):
		obj = self.request.user
		return obj
		
	def update(self, request, *args, **kwargs):
		self.object = self.get_object()
		serializer = self.get_serializer(data=request.data)

		if serializer.is_valid():
			if not self.object.check_password(serializer.data.get("old_password")):
				return Response({"old_password": ["誤ったパスワードです."]}, status=status.HTTP_400_BAD_REQUEST)
			self.object.set_password(serializer.data.get("new_password"))
			special_characters = """!@#$%^&*()-+?_=,<>/"""
			new_password=request.data.get('new_password')
			if any(i in special_characters for i in new_password) and any(char.isalpha() for char in new_password) and any(char.isdigit() for char in new_password):
				self.object.save()
				response = {'status': 'success', 'code': status.HTTP_200_OK, 'message': 'パスワードの更新が完了しました'}
				return Response(response)
			else:
				return Response({"password":"パスワードは半角英数でご入力ください."}, status=status.HTTP_400_BAD_REQUEST) 
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PatientLoginApiView(APIView):
	@swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING,
                                           description='email'),
                'password': openapi.Schema(type=openapi.TYPE_STRING,
                                          description='password'),
            },
            required=['email', 'password'],
        ),
        responses={status.HTTP_200_OK:UserSerializer}
    )
	def post(self, request):
		special_characters = """!@#$%^&*()-+?_=,<>/"""
		email = request.data.get('email')
		password = request.data.get('password')
		if password==None or password=="":
			return Response({'login':'ログインパスワードは必須です.'}, status=status.HTTP_400_BAD_REQUEST)
		if email==None or email=="":
			return Response({'email':'メールアドレスは必須です.'}, status=status.HTTP_400_BAD_REQUEST)
		if any(char.isalpha() for char in password) and any(char.isdigit() for char in password) and any(char in special_characters for char in password):
			user = User.objects.filter(email=email,is_patient=True,is_email_verified=True)
			if user.count():
				user = user.first()
			else:
				return Response('無効なユーザー', status=status.HTTP_401_UNAUTHORIZED)
			try:
				password=user.check_password(password)
				if not password:
					return Response('IDとパスワードが一致しません。再度お試しください.', status=status.HTTP_401_UNAUTHORIZED)
			except:
				return Response('登録されていないメールアドレスです。', status=status.HTTP_406_NOT_ACCEPTABLE)
			return Response(UserSerializer(user).data)
		else:
			return Response({'password':'パスワードは半角英数でご入力ください.'}, status=status.HTTP_400_BAD_REQUEST)

class PharmacyLoginApiView(APIView):
	@swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING,
                                           description='email'),
                'password': openapi.Schema(type=openapi.TYPE_STRING,
                                          description='password'),
            },
            required=['email', 'password'],
        ),
        responses={status.HTTP_200_OK:UserSerializer}
    )
	def post(self, request):
		from drugstore.models import DrugStore
		from drugstore.serializers import DrugStoreUserManagementSerializer
		special_characters = """!@#$%^&*()-+?_=,<>/"""
		email = request.data.get('email')
		password = request.data.get('password')
		if password==None or password=="":
			return Response({'login':'ログインパスワードは必須です.'}, status=status.HTTP_400_BAD_REQUEST)
		if email==None or email=="":
			return Response({'email':'メールアドレスは必須です.'}, status=status.HTTP_400_BAD_REQUEST)
		if any(char.isalpha() for char in password) and any(char.isdigit() for char in password) and any(char in special_characters for char in password):
			try:
				login_data = dict()
				user = User.objects.get(email=email,is_pharmacy=True,is_email_verified=True)
				password=user.check_password(password)
				drug_store_instance = DrugStore.objects.filter(user=user)
				login_data["drugstore"] = None
				if drug_store_instance:
					drug_store_instance= drug_store_instance.first()
					login_data["drugstore"] = DrugStoreUserManagementSerializer(drug_store_instance).data
				if not password:
					return Response('IDとパスワードが一致しません。再度お試しください.', status=status.HTTP_401_UNAUTHORIZED)
			except:
				return Response('登録されていないメールアドレスです。', status=status.HTTP_406_NOT_ACCEPTABLE)			
			login_data["user_data"] = UserSerializer(user).data
			return Response(data=login_data,status=status.HTTP_200_OK)
		else:
			return Response({'password':'パスワードは半角英数でご入力ください.'}, status=status.HTTP_400_BAD_REQUEST)

class CMSLoginApiView(APIView):
	@swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING,
                                           description='email'),
                'password': openapi.Schema(type=openapi.TYPE_STRING,
                                          description='password'),
            },
            required=['email', 'password'],
        ),
        responses={status.HTTP_200_OK:UserSerializer}
    )
	def post(self, request):
		special_characters = """!@#$%^&*()-+?_=,<>/"""
		email = request.data.get('email')
		password = request.data.get('password')
		if password==None or password=="":
			return Response({'login':'ログインパスワードは必須です.'}, status=status.HTTP_400_BAD_REQUEST)
		if email==None or email=="":
			return Response({'email':'メールアドレスは必須です.'}, status=status.HTTP_400_BAD_REQUEST)
		if any(char.isalpha() for char in password) and any(char.isdigit() for char in password) and any(char in special_characters for char in password):
			try:
				user = User.objects.get(email=email,is_orthrus=True,is_superuser=True,is_email_verified=True)
				password=user.check_password(password)
				if not password:
					return Response('IDとパスワードが一致しません。再度お試しください.', status=status.HTTP_401_UNAUTHORIZED)
			except:
				return Response('IDとパスワードが一致しません。再度お試しください.', status=status.HTTP_401_UNAUTHORIZED)
			return Response(UserSerializer(user).data)
		else:
			return Response({'password':'パスワードは半角英数でご入力ください.'}, status=status.HTTP_400_BAD_REQUEST)

class AdministratorStatusAPIView(APIView):
	def get(self, request):
		instance = AdministratorStatus.objects.all()
		return Response(data=AdministratorStatusSerializer(instance,many=True).data,status=status.HTTP_200_OK)

class LineAuthAPIView(APIView):
	"""
	Line Auth Registration/Login API

	Service Usage and Description: This API is used to create/update a user from Google callback and generate an auth token.

	Authentication Required: NO

	Data : {
		callback data from Line
		"token" : "Access Token from Line",
		"email" : "email"
	}

	Response : {
		"id": user_id,
		"email": email,
		"user_token": login_token,
	}    
	"""
	def post(self, request):
		data = request.data
		payload = {'access_token': data["token"]}
		#  "eyJhbGciOiJIUzI1NiJ9.p0Z8-x1drIBiRVIWDxkjhTfL3emxkVN7a_ByNpljLH09p3woF-DWv194TQCKF9cik3D0Lmbp6cggkDLGrX6FoiXnaPy86xKYspZwqoKtXwnpPfkM7kGd00zK9QoWY499GbONQMgElLFNFlkgZdQy1l7q2owlmdArJuLfF2s5_9k.fJgu18bnRA4omsXlFp8qYbnn9nZnuD3pMMk30CdAFZE"}  # validate the token
		verify_url ='https://api.line.me/oauth2/v2.1/verify'
		r = requests.get(verify_url, params=payload)
		r_data = json.loads(r.text)

		if 'error' in r_data:
			content = {'message': 'wrong line access token / access token expired'}
			return Response(content,status=status.HTTP_400_BAD_REQUEST)
		else:
			if "token" in data:
				if "email" in data:
					import uuid
					uid = uuid.uuid4()
					password = uid.hex
					email = data['email']
					user_objs = User.objects.filter(email=email,is_patient=True)
					if user_objs.count():
						user= user_objs.first()
					else:
						user = User.objects.create(email=email,is_patient=True)
						r = requests.get('https://api.line.me/oauth2/v2.1/userinfo', params=payload)
						user_data = json.loads(r.text)
						if 'error' in user_data:
							user.username=email
						else:
							user.username=user_data["name"]
						user.set_password(password)
						user.save()
					user_token, created = Token.objects.get_or_create(user=user)
					return Response(UserSerializer(user).data)
				else:
					content = {'message': 'Token Verified'}
					return Response(content,status=status.HTTP_200_OK)
			return Response({"message":"Token is required"},status=status.HTTP_400_BAD_REQUEST)

class EmailVerification(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'signup_verification.html'

    def get(self, request, *args, **kwargs):
        acc_id = self.request.GET.get("id")
        acc_objs = User.objects.filter(id=acc_id)
        if acc_objs.count():
            acc_obj = acc_objs[0]
            acc_obj.is_email_verified = True
            acc_obj.is_verification_updated = True
            acc_obj.save()
            user_token, created = Token.objects.get_or_create(user=acc_obj)
            if acc_obj.is_patient:
                # patient_id = acc_obj.patients.all()[0].id
                return HttpResponseRedirect(redirect_to='https://pharmacy-user.netlify.app/signUpComp?token={}&user_id={}'.format(user_token,acc_obj.id))
            else:
                return HttpResponseRedirect(redirect_to='https://dev-pharma-cms.eoraa.com/')
        return HttpResponseRedirect(redirect_to='https://pharmacy-user.netlify.app/evaluationfail')

class ResetPasswordVerification(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'reset_password.html'

    def get(self, request, *args, **kwargs):
        return render(request,'reset_password.html')

class DashboardAPIView(APIView):

	permission_classes = [IsCMS]

	def get(self, request, *args, **kwargs):
		data = {}
		user_usage_data ={}
		advertisement_objs = PharmaceuticalManufacturer.objects.all()
		advertise_serializer = AdvertisementDashboardSerializer(advertisement_objs,many=True)
		data["advertisement_status"] = advertise_serializer.data
		
		pharmacy_objs = Inquiry.objects.filter(inquiry_pharmacy__isnull=False,is_resolved=False)
		pharmacy_serializer = InquiryPharmacySerializer(pharmacy_objs,many=True)
		user_usage_data["Pharmacy"] = pharmacy_serializer.data
		
		patient_user_objs = Inquiry.objects.filter(inquiry_user__is_patient=True,is_resolved=False)
		patient_user_serializer = InquiryPatientSerializer(patient_user_objs,many=True)
		user_usage_data["Patient"] = patient_user_serializer.data
		data["user_usage"] = user_usage_data
		return Response(data,status=status.HTTP_200_OK)