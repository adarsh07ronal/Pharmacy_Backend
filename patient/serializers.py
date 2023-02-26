from rest_framework import serializers
from patient.models import Patient, PatientInsurance, Address, PatientDocument, Prescription,PrescriptionReceiptReservation
from pharmacy_auth.models import User

class PatientSerializer(serializers.ModelSerializer):
	class Meta:
		model = Patient
		fields = '__all__'

class PatientInsuranceSerializer(serializers.ModelSerializer):
	class Meta:
		model = PatientInsurance
		fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):
	class Meta:
		model = Address
		fields = '__all__'

class PatientDocumentSerializer(serializers.ModelSerializer):
	class Meta:
		model = PatientDocument
		fields = '__all__'

class PrescriptionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Prescription
		fields = '__all__'

class PrescriptionRetriveSerializer(serializers.ModelSerializer):
	prescription_image = serializers.SerializerMethodField('get_image_url')
	class Meta:
		model = Prescription
		exclude = ("patient",)

	def get_image_url(self, obj):
		if obj.prescription_image:
			return "https://dev-pharmacy.eoraa.com"+obj.prescription_image.url
		else:
			return None

class PrescriptionCreateRetriveSerializer(serializers.ModelSerializer):
	prescription_image = serializers.SerializerMethodField('get_image_url')
	class Meta:
		model = Prescription
		fields = "__all__"

	def get_image_url(self, obj):
		if obj.prescription_image:
			return "https://dev-pharmacy.eoraa.com"+obj.prescription_image.url
		else:
			return None

class UsermemoUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("password","groups","user_permissions")

class PrescriptionReceiptReservationSerializer(serializers.ModelSerializer):
	class Meta:
		model = PrescriptionReceiptReservation
		fields = '__all__'

class PrescriptionCalenderSerializer(serializers.ModelSerializer):
	class Meta:
		model = Prescription
		# fields = '__all__'
		exclude = ("patient",)


class PatientAndPatientInsurenceSerializer(serializers.ModelSerializer):
	patient_insurance = PatientInsuranceSerializer(many=True)

	class Meta:
		model = Patient
		fields = "__all__"


	def create(self, validated_data):
		insurance_data =  self.context['insurance_data']
		if "patient_insurance" in validated_data:
			validated_data.pop('patient_insurance')
		patient_instance = Patient.objects.create(**validated_data)
		serializer = PatientInsuranceSerializer(data=insurance_data,many=True,partial=True)
		if serializer.is_valid():
			serializer.save(patient=patient_instance)
		else:
			print(serializer.errors)
		return patient_instance

class PatientInformationSerializer(serializers.ModelSerializer):
	address = AddressSerializer()
	patient_insurance = PatientInsuranceSerializer(many=True)

	class Meta:
		model = Patient
		fields = ("id","name","nickname","dob","gender","address","phone_no","email","allergy_info","allergy_reactive","patient_insurance","is_linked","comment","key_matter_information")

class PatientInformationPharmacySerializer(serializers.ModelSerializer):
	address = AddressSerializer()
	patient_insurance = PatientInsuranceSerializer(many=True)
	prescription = PrescriptionCalenderSerializer(many=True)
	password = serializers.SerializerMethodField('get_user_password')

	def get_user_password(self, obj):
		user = obj.user
		return user.password
		
	class Meta:
		model = Patient
		fields = ("id","name","nickname","dob","gender","password","address","phone_no","email","allergy_info","allergy_reactive","patient_insurance","prescription","is_linked","comment","key_matter_information")

class PatientInformationUserManagementSerializer(serializers.ModelSerializer):
	patient_insurance = PatientInsuranceSerializer(many=True)
	prescription = PrescriptionCalenderSerializer(many=True)
	class Meta:
		model = Patient
		fields = ("id","name","nickname","dob","gender","phone_no","email","allergy_info","allergy_reactive","patient_insurance","prescription","is_linked","comment","key_matter_information")

class PatientCMSInfoSearchSerializer(serializers.ModelSerializer):
	prescription = PrescriptionCalenderSerializer(many=True)
	class Meta:
		model = Patient
		fields = '__all__'