from rest_framework import serializers
from .models import PharmacyOTCInformation, DrugEfficacyClassification

class PharmacyOTCInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PharmacyOTCInformation
        fields = "__all__"

class DrugEfficacyClassificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrugEfficacyClassification
        fields = "__all__"

class PharmacyOTCRetrieveSerializer(serializers.ModelSerializer):
    drug_classification = DrugEfficacyClassificationSerializer()
    class Meta:
        model = PharmacyOTCInformation
        fields = "__all__"
# class PharmacyOTCdetailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PharmacyOTCDetial
#         # fields = "__all__"
#         exclude = ("pharma_otc",)