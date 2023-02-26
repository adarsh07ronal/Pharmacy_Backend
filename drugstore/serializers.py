from rest_framework import serializers
from .models import DrugStore, Prefecture, User

class PrefectureSerializer(serializers.ModelSerializer):
	prefecture_rank =serializers.SerializerMethodField('get_pref_rank')
	
	def get_pref_rank(self, obj, *args,**kwargs):
		if obj.prefecture_rank:
			return f"{obj.prefecture_rank:02d}"
		return 0
	
	class Meta:
		model = Prefecture
		fields = '__all__'

class DSUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['id','email','password']

class DrugStoreSerializer(serializers.ModelSerializer):
	prefectures = PrefectureSerializer()
	user =DSUserSerializer()
	# representative =DSUserSerializer()

	# def create(self, validated_data):
	# 	prefecture_data  = validated_data.pop('prefectures')
	# 	print(prefecture_data)
	# 	prefecture = Prefecture.objects.create(**prefecture_data)
	# 	# user_data = validated_data.pop('representative')
	# 	# user = User.objects.create(**user_data)
	# 	drug_store = DrugStore.objects.create(**validated_data)
	# 	return drug_store

	class Meta:
		model = DrugStore
		fields = '__all__'
		# depth = 1

class DrugStoreCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = DrugStore
		fields = '__all__'

class DrugStoreUserManagementSerializer(serializers.ModelSerializer):
	prefectures = PrefectureSerializer()
	# representative =DSUserSerializer()

	class Meta:
		model = DrugStore
		exclude = ("user",)