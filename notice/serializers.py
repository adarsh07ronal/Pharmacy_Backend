from notice.models import Notice, NotificeDeliveryChoices, NotificeStatusChoices
from rest_framework import serializers

class NoticeCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Notice
		fields = '__all__'

class NoticeStatusSerializer(serializers.ModelSerializer):
	class Meta:
		model = NotificeStatusChoices
		fields = '__all__'

class NoticeDeliverySerializer(serializers.ModelSerializer):
	class Meta:
		model = NotificeDeliveryChoices
		fields = '__all__'

class NoticeSerializer(serializers.ModelSerializer):
	status=NoticeStatusSerializer()
	delivery_target=NoticeDeliverySerializer()
	class Meta:
		model = Notice
		fields = '__all__'