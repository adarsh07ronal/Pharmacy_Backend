from rest_framework import serializers
from drug.models import Medicine, MedicineEfficacyClassification


class MedicineSerializer(serializers.ModelSerializer):
	class Meta:
		model = Medicine
		fields = '__all__'

class DCSerializer(serializers.ModelSerializer):
	class Meta:
		model = MedicineEfficacyClassification
		fields = '__all__'

class MedicineRetrieveSerializer(serializers.ModelSerializer):
	drug_classification = DCSerializer()
	class Meta:
		model = Medicine
		fields = '__all__'