from .models import *
from rest_framework import serializers

class MedicineTipsSerializer(serializers.ModelSerializer):
	class Meta:
		model = MedicineTips
		fields = '__all__'

class MedicineTipsCategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = MedicineTipsCategory
		fields = '__all__'

class MedicineTipsRtrieveSerializer(serializers.ModelSerializer):
	image_registration = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)
	category=MedicineTipsCategorySerializer()

	class Meta:
		model = MedicineTips
		fields = '__all__'