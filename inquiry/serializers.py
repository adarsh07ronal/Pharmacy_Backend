from rest_framework import serializers
from inquiry.models import Inquiry, InquiryMessage
from drugstore.serializers import DSUserSerializer, DrugStoreSerializer

class InquirySerializer(serializers.ModelSerializer):
	class Meta:
		model = Inquiry
		fields = '__all__'

class InquiryPatientSerializer(serializers.ModelSerializer):
	patient_id =serializers.SerializerMethodField('get_user_patient_id')

	def get_user_patient_id(self, obj):
		patient_id = None
		if obj.inquiry_user.patients.all():
			patient_id = obj.inquiry_user.patients.all()[0].id
		return patient_id

	class Meta:
		model = Inquiry
		fields = '__all__'

class InquiryPharmacySerializer(serializers.ModelSerializer):
	pharmacy_id =serializers.SerializerMethodField('get_user_pharmacy_id')

	def get_user_pharmacy_id(self, obj):
		pharmacy_id = None
		if obj.inquiry_pharmacy:
			pharmacy_id = obj.inquiry_pharmacy.id
		return pharmacy_id

	class Meta:
		model = Inquiry
		fields = '__all__'

class InquiryMessageSerializer(serializers.ModelSerializer):
	class Meta:
		model = InquiryMessage
		fields = '__all__'

class InquiryRetrieveSerializer(serializers.ModelSerializer):
	inquiry_user = DSUserSerializer()
	inquiry_messages = InquiryMessageSerializer(many=True)
	inquiry_pharmacy = DrugStoreSerializer()

	class Meta:
		model = Inquiry
		fields = '__all__'

class InquiryRetrieveRegisteredUserSerializer(serializers.ModelSerializer):
	inquiry_messages = InquiryMessageSerializer(many=True)
	class Meta:
		model = Inquiry
		exclude =("inquiry_user","inquiry_pharmacy")