
from rest_framework import serializers
from .models import FavoriteDrugStore
from patient.serializers import PatientSerializer
from drugstore.serializers import DrugStoreSerializer

class FavoriteDrugStoreCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = FavoriteDrugStore
		fields = '__all__'

class FavoriteDrugStoreSerializer(serializers.ModelSerializer):
    patient = PatientSerializer()
    drugstore = DrugStoreSerializer()
    class Meta:
        model = FavoriteDrugStore
        fields = '__all__'