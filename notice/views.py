from rest_framework import viewsets
from notice.models import *
from notice.serializers import *

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg import openapi
from rest_framework.parsers import MultiPartParser, JSONParser
# from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from itertools import chain
from rest_framework.pagination import PageNumberPagination


# Create your views here.
class NoticeViewSet(viewsets.ModelViewSet):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    parser_classes = (MultiPartParser,JSONParser)
    # pagination_class=None
    
    def update(self, request, *args,**kwargs):
        try:
            data = self.request.data
            notice_instance = Notice.objects.filter(id=self.kwargs["pk"])
            if notice_instance.count():
                notice_instance = notice_instance.first()
                if "status" in data:
                    status_instance = NotificeStatusChoices.objects.filter(id=data["status"])
                    if status_instance.count():
                        status_instance = status_instance.first()
                        if status_instance.status_choice == 3:
                            notice_instance.delete()
                            return Response(status=status.HTTP_200_OK)	
                serializer = NoticeCreateSerializer(notice_instance,data=data,partial=True)
                if serializer.is_valid():
                    instance = serializer.save()
                    return Response(data=NoticeSerializer(instance).data,status=status.HTTP_202_ACCEPTED)	
                else:
                    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message":"お知らせのデータが見つかりません"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class NoticeListingAPIView(APIView,PageNumberPagination):
    
    def get(self,request,*args,**kwargs):
        user=self.request.user
        all_users_notice_objs = Notice.objects.filter(delivery_target__delivery_target_choice=1,status__status_choice=1)
        next_list = []
        if user.is_authenticated:
            if user.is_patient:
                next_list = Notice.objects.filter(delivery_target__delivery_target_choice=3,status__status_choice=1)
            elif user.is_pharmacy:
                next_list = Notice.objects.filter(delivery_target__delivery_target_choice=4,status__status_choice=1)
        else:
            next_list = Notice.objects.filter(delivery_target__delivery_target_choice=2,status__status_choice=1)
        result_list = all_users_notice_objs.union(next_list)
        # return Response(data=NoticeSerializer(result_list,many=True).data,status=status.HTTP_200_OK)
        return self.get_paginated_response(NoticeSerializer(self.paginate_queryset(result_list,request),many=True).data)

class NoticeCreateAPIView(APIView):
    """
    Notice Create APIView
    
    Request Data : {
        "title" : "Title",
        "text" : "text",
        "status" : 1,
        "delivery_target" : 1,
        "deliver_start_time" : "2022-05-10",
        "deliver_end_time" : "2022-05-10",
        "image_registration" : Upload an Image,
    }
    """
    parser_classes = [MultiPartParser,JSONParser]
    permission_classes = [IsAuthenticated]

    def post(self,request,*args,**kwargs):
        try:
            data = request.data
            serializer = NoticeCreateSerializer(data=data,partial=True)
            if serializer.is_valid():
                instance = serializer.save()
                return Response(data=NoticeSerializer(instance).data,status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class NoticeUpdateAPIView(APIView):
    """
    Notice Update APIView

    Request Data : {
        "title" : "Title",
        "text" : "text",
        "status" : 1,
        "delivery_target" : 1,
        "deliver_start_time" : "2022-05-10",
        "deliver_end_time" : "2022-05-10",
        "image_registration" : Upload an Image,
    }

    """
    parser_classes = [MultiPartParser,JSONParser]
    
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING,description='title'),
                'text': openapi.Schema(type=openapi.TYPE_STRING,description='text'),
                'status': openapi.Schema(type=openapi.TYPE_INTEGER,description='status'),
                'delivery_target': openapi.Schema(type=openapi.TYPE_INTEGER,description='delivery_target'),
                'deliver_start_time': openapi.Schema(type=openapi.TYPE_STRING,description='deliver_start_time'),
                'deliver_end_time': openapi.Schema(type=openapi.TYPE_STRING,description='deliver_end_time'),
                'image_registration': openapi.Schema(type=openapi.TYPE_STRING,description='image_registration')
            },
        ),
        responses={status.HTTP_200_OK:NoticeSerializer}
    )

    def put(self,request,*args,**kwargs):
        try:
            data = request.data
            pk = self.kwargs['pk']
            instances = Notice.objects.filter(id=pk)
            if instances.count():
                instance = instances.first()
                serializer = NoticeCreateSerializer(instance,data=data,partial=True)
                if serializer.is_valid():
                    instance = serializer.save()
                    return Response(data=NoticeSerializer(instance).data,status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            return Response({"message":"お知らせのデータが見つかりません"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class NoticeDeliveryAndStatusAPIView(APIView):
    def get(self,request,*args,**kwargs):
        data_l = dict()
        status_queryset = NotificeStatusChoices.objects.all()
        delivery_queryset = NotificeDeliveryChoices.objects.all()
        data_l["status"] = (NoticeStatusSerializer(status_queryset,many=True).data)
        data_l["delivery_target"]=(NoticeDeliverySerializer(delivery_queryset,many=True).data)
        return Response(data=data_l,status=status.HTTP_200_OK)