from drugstore.models import DrugStore
from rest_framework import serializers
from inquiry.serializers import InquiryRetrieveRegisteredUserSerializer
from pharmacy_auth.models import User, Otp,AdministratorStatus
from drugstore.serializers import DSUserSerializer,PrefectureSerializer
from patient.serializers import PatientInformationPharmacySerializer

class UserSerializer(serializers.ModelSerializer):
	user_token = serializers.SerializerMethodField(source='get_user_token')

	class Meta:
		model = User
		fields = ['id','email', 'user_token']

	def get_user_token(self, obj):
		user_token = obj.auth_token
		return user_token.key

class UserManagementSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['id','email','username','is_administrator','is_editor','is_viewer']

class CMSUserCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = '__all__'

class CMSUserSerializer(serializers.ModelSerializer):
	user_token = serializers.SerializerMethodField(source='get_user_token')
	class Meta:
		model = User
		fields = ['id','email','username','is_administrator','is_editor','is_viewer','user_token']
	def get_user_token(self, obj):
		user_token = obj.auth_token
		return user_token.key

class UserPatientSerializer(serializers.ModelSerializer):
	user_token = serializers.SerializerMethodField(source='get_user_token')
	password = serializers.CharField(write_only=True, required=True)

	class Meta:
		model = User 
		fields = ['email','password', 'user_token']

	def get_user_token(self, obj):
		user_token = obj.auth_token
		return user_token.key
		

class UserOrthrusSerializer(serializers.ModelSerializer):
	user_token = serializers.SerializerMethodField(source='get_user_token')
	password = serializers.CharField(write_only=True, required=False)

	class Meta:
		model = User
		fields = ['email', 'password', 'user_token']

	def get_user_token(self, obj):
		user_token = obj.auth_token
		return user_token.key

class UserPharmacySerializer(serializers.ModelSerializer):
	user_token = serializers.SerializerMethodField(source='get_user_token')
	password = serializers.CharField(write_only=True, required=False)

	class Meta:
		model = User
		fields = ['email', 'password', 'user_token']

	def get_user_token(self, obj):
		user_token = obj.auth_token
		return user_token.key

class OtpSerializer(serializers.ModelSerializer):
	class Meta:
		model = Otp
		fields = '__all__'

class ChangePasswordSerializer(serializers.Serializer):
	old_password = serializers.CharField(required=True)
	new_password = serializers.CharField(required=True)

	class Meta:
		model = User

class AdministratorStatusSerializer(serializers.Serializer):
	class Meta:
		model = AdministratorStatus

class RegisteredUserSerializer(serializers.ModelSerializer):
	user_inquiries=InquiryRetrieveRegisteredUserSerializer(many=True)
	patients = PatientInformationPharmacySerializer(many=True)

	# def get_inquiries(self,instance):
	# 	qs = instance.user_inquiries.all().order_by('updated_at')
	# 	return InquiryRetrieveRegisteredUserSerializer(qs,many=True).data

	class Meta:
		model = User
		fields = ['id','email','username','is_patient','user_inquiries','patients']

class RegisteredPharmacySerializer(serializers.ModelSerializer):
	user = DSUserSerializer()
	prefectures = PrefectureSerializer()
	pharmacy_inquiries=InquiryRetrieveRegisteredUserSerializer(many=True)
	# =serializers.SerializerMethodField('get_inquiries')
	
	# def get_inquiries(self,instance):
	# 	qs = instance.pharmacy_inquiries.all().order_by('updated_at')
	# 	return InquiryRetrieveRegisteredUserSerializer(qs,many=True).data

	class Meta:
		model = DrugStore
		# fields = ['id','email','pharmacy_inquiries','user','representative','','','']
		fields = "__all__"