from rest_framework import serializers
from .models import *
from message.models import ReservationMessage
from message.serializers import UserMemoMessageRetrieveSerializer
from patient.serializers import PrescriptionSerializer, AddressSerializer, PatientInsuranceSerializer,PatientDocumentSerializer, UsermemoUserSerializer,PatientSerializer
from patient.models import Patient
from drugstore.serializers import DSUserSerializer,DrugStoreSerializer
from drugstore.models import DrugStore

class ForReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForReservation
        fields = "__all__"

class MessageReservationSerializer(serializers.ModelSerializer):
    sender = DSUserSerializer()
    class Meta:
        model = ReservationMessage
        # fields = "__all__"
        exclude = ("prescription_reservation",)

class ReservationPatientSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    patient_insurance = PatientInsuranceSerializer(many=True)
    documents = PatientDocumentSerializer(many=True)
    class Meta:
        model = Patient
        fields = '__all__'

class PharmacySerializer(serializers.ModelSerializer):
    class Meta:
        model = DrugStore
        fields = ("id","drugstore_name")

class RecieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recieve_choice
        fields = "__all__"

class ForReservationCalendarSerializer(serializers.ModelSerializer):
    pharmacy = DrugStoreSerializer()
    receive_prescription_by = RecieveSerializer()
    class Meta:
        model = ForReservation
        # fields = "__all__"
        exclude = ('patient','prescription')

class ForReservationSearchSerializer(serializers.ModelSerializer):
    patient = ReservationPatientSerializer()
    reservation_messages = MessageReservationSerializer(many=True)
    prescription = PrescriptionSerializer(many=True)
    receive_prescription_by = RecieveSerializer()
    class Meta:
        model = ForReservation
        # fields = "__all__"
        exclude = ("pharmacy",)

class UserMemoForReservationSearchSerializer(serializers.ModelSerializer):
    prescription = PrescriptionSerializer(many=True)
    receive_prescription_by = RecieveSerializer()
    class Meta:
        model = ForReservation
        exclude = ("pharmacy","patient")

class UserMemoSerializer(serializers.ModelSerializer):
	pharmacy_name = serializers.SerializerMethodField('get_pharmacy_name')
	pharmacist= serializers.SerializerMethodField('get_pharmacist')
	user = UsermemoUserSerializer()
	prescription_reservation = UserMemoForReservationSearchSerializer()

	def get_pharmacy_name(self, obj, *args,**kwargs):
		if obj.pharmacy_name:
			return obj.pharmacy_name
		else:
			if obj.pharmacy:
				return obj.pharmacy.drugstore_name
			return ""
	
	def get_pharmacist(self, obj, *args,**kwargs):
		if obj.pharmacist:
			return obj.pharmacist
		else:
			if obj.pharmacy:
				if obj.pharmacy.representative:
					return obj.pharmacy.representative
			return ""

	class Meta:
		model = UserMemo
		fields = ("pharmacy_name","pharmacist","user","id","memo_scheduled_time","created_at","updated_at","pharmacy","prescription_reservation","is_usermemo_added","title","description")

class UserMemoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMemo
        fields = "__all__"

class UserMemoPrescriptionSerializer(serializers.ModelSerializer):
    pharmacy_name = serializers.SerializerMethodField('get_pharmacy_name')
    pharmacist= serializers.SerializerMethodField('get_pharmacist')
    memo_messages = UserMemoMessageRetrieveSerializer(many=True)

    def get_pharmacy_name(self, obj, *args,**kwargs):
        if obj.pharmacy_name:
            return obj.pharmacy_name
        else:
            if obj.pharmacy:
                return obj.pharmacy.drugstore_name
            return ""
    
    def get_pharmacist(self, obj, *args,**kwargs):
        if obj.pharmacist:
            return obj.pharmacist
        else:
            if obj.pharmacy:
                if obj.pharmacy.representative:
                    return obj.pharmacy.representative
            return ""

    class Meta:
        model = UserMemo
        fields = ("id","pharmacy_name","pharmacist","memo_scheduled_time","created_at","updated_at","memo_messages","title","description")

class ForReservationRetrieveSerializer(serializers.ModelSerializer):
    reservation_memos = UserMemoPrescriptionSerializer(many=True)
    reservation_messages = MessageReservationSerializer(many=True)
    patient = ReservationPatientSerializer()
    prescription = PrescriptionSerializer(many=True)
    pharmacy = DrugStoreSerializer()
    application_message = serializers.CharField(source='message')
    receive_prescription_by = RecieveSerializer()
    class Meta:
        model = ForReservation
        fields = "__all__"

class PrescriptionRetriveAllSerializer(serializers.ModelSerializer):
	memos = UserMemoPrescriptionSerializer(many=True)
	patient = PatientSerializer()
	prescription_image = serializers.SerializerMethodField('get_image_url')
	
	class Meta:
		model = Prescription
		fields = "__all__"
	def get_image_url(self, obj):
		if obj.prescription_image:
			return "https://dev-pharmacy.eoraa.com"+obj.prescription_image.url
		else:
			return None
