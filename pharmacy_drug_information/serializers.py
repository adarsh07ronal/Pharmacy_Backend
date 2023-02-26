from rest_framework import serializers
from .models import PharmacyDrugInformation

class PharmacyDrugInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PharmacyDrugInformation
        fields = "__all__"