from rest_framework import serializers
from .models import ReservationMessage, UserMemoMessage
from drugstore.serializers import DSUserSerializer

class ReservationMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model =ReservationMessage 
        fields = "__all__"

class ReservationMessageRetrieveSerializer(serializers.ModelSerializer):
    # prescription_reservation = ForReservationSerializer()
    sender = DSUserSerializer()
    class Meta:
        model =ReservationMessage 
        # fields = "__all__"
        exclude = ("prescription_reservation",)

class UserMemoMessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model =UserMemoMessage 
        fields = "__all__"

class UserMemoMessageRetrieveSerializer(serializers.ModelSerializer):
    sender = DSUserSerializer()
    class Meta:
        model =UserMemoMessage 
        exclude = ("usermemo",)