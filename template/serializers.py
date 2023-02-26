from rest_framework import serializers
from .models import *

class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        # fields = "__all__"
        exclude = ("user",)
 
class TemplateCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = "__all__"