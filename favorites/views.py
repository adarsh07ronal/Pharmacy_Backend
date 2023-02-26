from rest_framework.views import APIView
from drugstore.models import DrugStore
from .serializers import *
from .models import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

class DrugStoreFavoriteAPIView(APIView):
    """
    Drugstore Favorite API

    Authentication Required : YES

    Data : {
        "drugstore" : 1,
        "is_favorite" : 0/1,
        "patient" : 4441
    }
        
    """

    permission_classes = [IsAuthenticated]
    def post(self,request, format=None):
        try:
            data= self.request.data
            objs = FavoriteDrugStore.objects.filter(drugstore=data["drugstore"],patient=data["patient"])
            if objs.count():
                obj = objs.first()
                serializer = FavoriteDrugStoreCreateSerializer(obj,data=data,partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(data = FavoriteDrugStoreSerializer(obj).data ,status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors ,status=status.HTTP_400_BAD_REQUEST)
            else:
                pharmacy_objs = DrugStore.objects.filter(id=data["drugstore"])
                if pharmacy_objs.count():
                    serializer = FavoriteDrugStoreCreateSerializer(data=data,partial=True)
                    if serializer.is_valid():
                        instance = serializer.save()
                        return Response(data = FavoriteDrugStoreSerializer(instance).data ,status=status.HTTP_200_OK)
                    else:
                        return Response(serializer.errors ,status=status.HTTP_400_BAD_REQUEST)
                return Response({"message":"薬局のデータが見つかりません"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
