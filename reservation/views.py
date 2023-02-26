from rest_framework import viewsets
from .serializers import *
from .models import *
from message.models import ReservationMessage, TemplateReservationMessage
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
import ast
from template.models import Template
from reservation.serializers import ForReservationSearchSerializer
from django.db.models import Count
from django.db.models import Q
from message.models import UserMemoMessage
from message.serializers import UserMemoMessageCreateSerializer
from rest_framework.pagination import PageNumberPagination
from django.core.mail import send_mail
# Create your views here.

class MyPaginator(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'

class ForReservationViewset(viewsets.ModelViewSet):
    """
        Reservation List API 
        
        Params : {
            "reservation_id" : 1
        }

        Reservation Update API 
        
        Data : {
            "is_accepted" : true,
            "reservation_scheduled_time" : "",
            "medication_guidence" : true,
            "guidance_scheduled_time" : "",
            "template" : 1, (Optional)
            "message" : "Hello",
            "prescription" : [1,2] 
        }

        Reservation Create API 
        
        Data : {
            "reservation_scheduled_time" : "",
            "medication_guidence" : true,
            "guidance_scheduled_time" : "",
            "template" : 1, (Optional)
            "message" : "Hello",
            "prescription" : [1,2],
            "pharmacy: 1,
            "receive_prescription_by":1
        }
    """

    queryset = ForReservation.objects.all()
    serializer_class = ForReservationRetrieveSerializer
    lookup_field = "id"
    pagination_class = MyPaginator

    def create(self, request, *args, **kwargs):
        try:
            mutable = request.POST._mutable
            request.POST._mutable = True
            data = request.data
            mess_data = data["message"]
            # del data["message"]
            presc_data = None
            if "prescription" in data: 
                presc_data =data["prescription"]
                del data["prescription"]
            patient_objs = Patient.objects.filter(user=self.request.user)
            if patient_objs.count():
                patient_obj = patient_objs.first()
                data["patient"] = patient_obj.id
                serializer = ForReservationSerializer(data=data)
                if serializer.is_valid():
                    if data["medication_guidence"]:
                        instance = serializer.save(scheduled_by=self.request.user)
                    else:
                        instance = serializer.save(scheduled_by=self.request.user,remote_medication_scheduled_by=self.request.user)
                    pharmacy =instance.pharmacy
                    patient_obj.pharmacy_visited.add(pharmacy.id)
                    patient_obj.save()
                    user_memo_obj = UserMemo.objects.create(pharmacy_name=pharmacy.drugstore_name,pharmacist=pharmacy.representative,pharmacy=pharmacy,prescription_reservation=instance,user=instance.patient.user)
                    if presc_data:
                        if type(presc_data) == str:
                            for i in ast.literal_eval(presc_data):
                                instance.prescription.add(int(i))
                                # if data["medication_guidence"]:
                                user_memo_obj.prescription.add(int(i))
                        else:
                            for i in presc_data:
                                instance.prescription.add(int(i))
                                # if data["medication_guidence"]:
                                user_memo_obj.prescription.add(int(i))
                        instance.save()
                        user_memo_obj.save()

                    # try:
                    #     if data["medication_guidence"]:
                    #         send_mail(
                    #             '遠隔服薬指導の予約申請をおこないました',
                    #             "{} 様\n\n遠隔服薬指導の予約申請をおこないました。\n以下の日程となりますので、お忘れのないようにお願いいたします。\n{}\nなお、申請いただいた日程は、確定ではありません。\n{} にて確認の上、承諾があり次第確定となります。\n申請いただいた日程での実施ができない場合、修正依頼が届きますので、\nお手数ですが再設定をお願いいたします。\n\n////////////\nじぶん薬局運営事務局\n住所：〒254-0014\n神奈川県平塚市四之宮1-4-13\n\nE-mail：info@orthros.com".format(instance.patient.name,instance.guidance_scheduled_time,instance.pharmacy.drugstore_name),
                    #             'developers.geitpl@gmail.com',
                    #             [instance.patient.email,'karre@eoraa.com'],
                    #         )
                    # except:
                    #     pass

                    ReservationMessage.objects.create(sender=self.request.user,message=mess_data,prescription_reservation=instance)
                    return Response(data = ForReservationRetrieveSerializer(instance).data ,status=status.HTTP_201_CREATED)
                else:
                    return Response(data = serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message":"あなたは認可された患者ではありません"},status=status.HTTP_406_NOT_ACCEPTABLE)
        except Exception as e:
            return Response({"message":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR) 

    def list(self, request, *args, **kwargs):
        
        user_obj = self.request.user
        if user_obj.is_anonymous:
            qs=[]
            # return Response(data=ForReservationRetrieveSerializer(qs,many=True).data,status=status.HTTP_200_OK)
        else:
            if user_obj.is_patient:
                qs = ForReservation.objects.filter(patient__user=user_obj).order_by('-updated_at')
            elif user_obj.is_pharmacy:
                qs = ForReservation.objects.filter(pharmacy__user=user_obj).order_by('-updated_at')
            else:
                qs = ForReservation.objects.all()
        return self.get_paginated_response(ForReservationRetrieveSerializer(self.paginate_queryset(qs),many=True).data)
            # return Response(ForReservationRetrieveSerializer(qs,many=True).data,status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        mutable = request.POST._mutable
        request.POST._mutable = True
        self.object = self.get_object()
        data = request.data
        user_obj = self.request.user
        rm_f = 0
        a_f =0
        if self.object:
            if "is_accepted" in data:
                if not data["is_accepted"]:
                    data["scheduled_by"] = user_obj.id
                else:
                    if self.object.is_accepted:
                        a_f =1
            if "is_remote_accepted" in data:
                if not data["is_remote_accepted"]:
                    data["remote_medication_scheduled_by"] = user_obj.id
                else:
                    if self.object.is_remote_accepted:
                        rm_f =1
            if "prescription" in data: 
                if type(data["prescription"]) == str:
                    for i in ast.literal_eval(data["prescription"]):
                        self.object.prescription.add(int(i))
                else:
                    for i in data["prescription"]:
                        self.object.prescription.add(int(i))
                del data["prescription"]
            if "message" in data:
                mess_data = data["message"]
                if user_obj.is_patient:
                    res_mess = ReservationMessage.objects.create(sender=user_obj,message=mess_data,prescription_reservation=self.object,is_seen_pharmacy=False)
                elif user_obj.is_pharmacy:
                    res_mess = ReservationMessage.objects.create(sender=user_obj,message=mess_data,prescription_reservation=self.object,is_seen_patient=False)
                self.object.save()
                if "template" in data:
                    template_data = data["template"]
                    template_instance = Template.objects.filter(id=template_data)
                    if template_instance.count():
                        template_instance = template_instance.first()
                        TemplateReservationMessage.objects.create(template=template_instance,reservation_message=res_mess)
                    del data["template"]
                del data["message"]
            serializer = ForReservationSerializer(self.object,data=data,partial=True)
            if serializer.is_valid():
                instance = serializer.save()
                
                objs =  ReservationMessage.objects.filter(prescription_reservation__id=instance.id).exclude(id=res_mess.id)
                if user_obj.is_patient:
                    objs.update(is_seen_patient=True)
                    instance.is_seen_pharmacy=False
                    instance.is_seen_patient=True
                elif user_obj.is_pharmacy:
                    objs.update(is_seen_pharmacy=True)
                    instance.is_seen_patient=False
                    instance.is_seen_pharmacy=True
                instance.save()
                if "is_accepted" in data:   
                    if instance.is_accepted:
                        if a_f==0:
                            try:
                                send_mail(
                                    '処方箋受取の予約が確定しました',
                                    "{} 様\n\n{} 様の処方箋受取予約が確定しました。\n万一変更が必要になった場合には、予約管理画面より修正を行ってください。\n{}\n\n////////////\nじぶん薬局運営事務局\n住所：〒254-0014\n神奈川県平塚市四之宮1-4-13\nE-mail：info@orthros.com".format(instance.pharmacy.representative,instance.patient.name,"https://pharma-company.netlify.app/mypage"),
                                    'developers.geitpl@gmail.com',
                                    [instance.pharmacy.email,'karre@eoraa.com'],
                                )
                                reservation_date =str(instance.reservation_scheduled_time)
                                l=reservation_date.split("-")
                                ll =l[2].split(" ")
                                reservation_date=l[0]+"年"+l[1]+"月"+ll[0]+"日 "+ll[1][0:5]
                                send_mail(
                                    '処方箋の受取予約が確定しました',
                                    "{} 様\n\n処方箋受取予約日が確定しました。\n以下の日程となりますので、お忘れのないようにお受け取りください。\n\n日程\n{}\n\n申請いただいた日程での受取ができなくなってしまった場合には、\nお手数ですが処方箋受取日の修正申請ををお願いいたします。\n{}\n\n////////////\nじぶん薬局運営事務局\n住所：〒254-0014\n神奈川県平塚市四之宮1-4-13\nE-mail：info@orthros.com".format(instance.patient.name,reservation_date,'https://pharmacy-user.netlify.app/mypage'),
                                    'developers.geitpl@gmail.com',
                                    [instance.patient.email,'karre@eoraa.com'],
                                )
                            except Exception as e:
                                return Response({"message":str(e)},status=status.HTTP_400_BAD_REQUEST)
                    else:
                        try:
                            # if rm_f == 0:
                                # TEMP 06
                            reservation_date =str(instance.reservation_scheduled_time)
                            l=reservation_date.split("-")
                            ll =l[2].split(" ")
                            reservation_date=l[0]+"年"+l[1]+"月"+ll[0]+"日 "+ll[1][0:5]
                            send_mail('処方箋受取の予約修正申請をおこないました','{} 様 \n\n 処方箋受取の修正予約申請をおこないました。 以下の日程となりますので、お忘れのないようにお受け取りください。\n\n日程\n{}\n\n なお、申請いただいた日程は、まだ確定ではありません。{} にて確認の上、承諾があり次第確定となります。 \n\n 申請いただいた日程での受取ができない場合、再度の修正依頼が届きますので、 お手数ですが再設定をお願いいたします。\n\n////////////\nじぶん薬局運営事務局\n住所：〒254-0014\n神奈川県平塚市四之宮1-4-13\nE-mail：info@orthros.com'.format(instance.patient.name,reservation_date,instance.pharmacy.drugstore_name),'developers.geitpl@gmail.com',[instance.patient.email,'karre@eoraa.com'])

                            # TEMP 18
                            send_mail('処方箋受取の予約が修正申請されました','{} 様\n{} 様より、処方箋受取の修正予約申請が届きました。予約管理画面より修正予約をご確認いただき、承認または再修正手続きを 行っていただけますよう、よろしくお願いいたします。\n{}\n\n////////////\nじぶん薬局運営事務局\n住所：〒254-0014\n神奈川県平塚市四之宮1-4-13\nE-mail：info@orthros.com'.format(instance.pharmacy.representative,instance.patient.name,"https://pharma-company.netlify.app/mypage"),'developers.geitpl@gmail.com',[instance.pharmacy.email,'karre@eoraa.com'])
                        except Exception as e:
                            return Response({"message":str(e)},status=status.HTTP_400_BAD_REQUEST)   
                if "is_remote_accepted" in data:
                    if not data["is_remote_accepted"]:
                        try:
                            guidance_date =str(instance.guidance_scheduled_time)
                            l=guidance_date.split("-")
                            ll =l[2].split(" ")
                            guidance_date=l[0]+"年"+l[1]+"月"+ll[0]+"日 "+ll[1][0:5]
                            send_mail(
                                '遠隔服薬指導の予約修正申請をおこないました',
                                "{} 様\n\n遠隔服薬指導の修正予約申請をおこないました。\n以下の日程となりますので、お忘れのないようにお願いいたします。\n\n日程\n{}\n\nなお、申請いただいた日程は、確定ではありません。\n{} にて確認の上、承諾があり次第確定となります。\n申請いただいた日程での実施ができない場合、再度の修正依頼が届きますので、\nお手数ですが再設定をお願いいたします。\n\n////////////\nじぶん薬局運営事務局\n住所：〒254-0014\n神奈川県平塚市四之宮1-4-13\nE-mail：info@orthros.com".format(instance.patient.name,guidance_date,instance.pharmacy.drugstore_name),
                                'developers.geitpl@gmail.com',
                                [instance.patient.email,'karre@eoraa.com'],
                            )
                            send_mail(
                                '遠隔服薬指導の予約が修正申請されました',
                                "{} 様\n\n{} 様より、遠隔服薬指導の修正予約申請が届きました。\n予約管理画面より予約をご確認いただき、承認または再度の修正手続きを\n行っていただけますよう、よろしくお願いいたします。\n{}\n\n////////////\nじぶん薬局運営事務局\n住所：〒254-0014\n神奈川県平塚市四之宮1-4-13\nE-mail：info@orthros.com".format(instance.pharmacy.representative,instance.patient.name,'https://pharma-company.netlify.app/mypage'),
                                'developers.geitpl@gmail.com',
                                [instance.pharmacy.email,'karre@eoraa.com'],
                            )
                        except Exception as e:
                            return Response({"message":str(e)},status=status.HTTP_400_BAD_REQUEST)
                    else:
                        if rm_f == 0:
                            try:
                                send_mail(
                                    '遠隔服薬指導の実施日が確定しました',
                                    "{} 様\n\n遠隔服薬指導の実施日が確定しました。\n以下の日程となりますので、お忘れのないようにお願いいたします。\n\n遠隔服薬指導日時になりましたら、以下のURLからサイトにアクセスいただき、\n遠隔服薬指導を実施してください。\n{}\n\nなお、遠隔服薬指導の実施日を変更されたい場合は、以下のURLから\n変更手続きをお願いいたします。\n{}\n\n////////////\nじぶん薬局運営事務局\n住所：〒254-0014\n神奈川県平塚市四之宮1-4-13\nE-mail：info@orthros.com".format(instance.patient.name,"http://pharmacy-user.netlify.app/","https://pharmacy-user.netlify.app/mypage/reserve/{}".format(instance.id)),
                                    'developers.geitpl@gmail.com',
                                    [instance.patient.email,'karre@eoraa.com'],
                                )

                                send_mail(
                                    '遠隔服薬指導の実施予約が確定しました',
                                    "{} 様\n\n{} 様の遠隔服薬指導実施日が確定しました。\n万一変更が必要になった場合には、予約管理画面より修正を行ってください。\n{}\n\n////////////\nじぶん薬局運営事務局\n住所：〒254-0014\n神奈川県平塚市四之宮1-4-13\nE-mail：info@orthros.com".format(instance.pharmacy.representative,instance.patient.name,"https://pharma-company.netlify.app/mypage"),
                                    'developers.geitpl@gmail.com',
                                    [instance.pharmacy.email,'karre@eoraa.com'],
                                )
                            except Exception as e:
                                return Response({"message":str(e)},status=status.HTTP_400_BAD_REQUEST)
                return Response(data=ForReservationRetrieveSerializer(instance).data,status=status.HTTP_202_ACCEPTED)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class GuidanceMessageViewset(viewsets.ModelViewSet):
    """
        Guidance Message API 
        
        Data : {
            "usermemo" : 1,
            "title" : "",
            "message" : "",
            "memo_scheduled_time" : "2022-06-04"
        }
    """

    queryset = UserMemoMessage.objects.all()
    serializer_class = UserMemoMessageCreateSerializer

    def create(self, request, *args, **kwargs):
        mutable = request.POST._mutable
        request.POST._mutable = True
        data = request.data
        user_obj = self.request.user
        data["sender"] = user_obj.id
        if "memo_scheduled_time" in data:
            usermemo_objs = UserMemo.objects.filter(id=data["usermemo"])
            if usermemo_objs.count():
                usermemo_obj = usermemo_objs.first()
                usermemo_obj.memo_scheduled_time = data["memo_scheduled_time"]
                usermemo_obj.save()
            del data["memo_scheduled_time"]
        serializer = UserMemoMessageCreateSerializer(data=data,partial=True)
        if serializer.is_valid():
            instance = serializer.save()
            return Response(data=UserMemoMessageCreateSerializer(instance).data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class ForReservationReplyAPI(APIView):
    """
        REQUEST DATA : {
            "is_accepted": True/False,
            "reservation_scheduled_time" : "",
            "medication_guidence": True/False,
            "guidance_scheduled_time":"",
            "template" : 1, 
            "message" :"HELLOO"
        }

    """
    def post(self, request, *args, **kwargs):
        try:
            mutable = request.POST._mutable
            request.POST._mutable = True
            data = request.data
            res_data = {
                "is_accepted" : data["is_accepted"],
                "reservation_scheduled_time" : data["reservation_scheduled_time"],
                "medication_guidence" : data["medication_guidence"],
                "guidance_scheduled_time": data["guidance_scheduled_time"]
            }
            serializer = ForReservationSerializer(data=res_data,partial=True)
            if serializer.is_valid():
                instance = serializer.save()
                if "message" in data:
                    res_mess = ReservationMessage.objects.create(sender=self.request.user,message=data["message"],prescription_reservation=instance)
                if "template" in data:
                    TemplateReservationMessage.objects.create(template=data["template"],reservation_message=res_mess)
                return Response(data = ForReservationRetrieveSerializer(instance).data ,status=status.HTTP_201_CREATED)
            else:
                return Response(data = serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR) 

class RecieveChoiceAPIView(APIView):
    def get(self,request,*args,**kwargs):
        recieve_ins = Recieve_choice.objects.all()
        recieve_serializer = RecieveSerializer(recieve_ins,many=True)
        return Response(data=recieve_serializer.data, status=status.HTTP_200_OK)        

class PrescriptionReservationSearchAPI(APIView):
    """
    Prescription Reservation Search API

    Authentication Required : YES

    Request Data: {
        "start_date":"",
        "end_date":"",
        "filter_category":1,
        "patient":"",
    }

    """

    permission_classes = [IsAuthenticated]
    def post(self,request, *args, **kwargs):
        try:
            mutable = request.POST._mutable
            request.POST._mutable = True
            data = self.request.data
            reservation_objs = ForReservation.objects.filter(pharmacy__user=self.request.user)
            if reservation_objs.count():
                if "start_date" in data:
                    if data["start_date"]:
                        if "end_date" in data:
                            if data["end_date"]:
                                reservation_objs = reservation_objs.filter(created_at__range=[data["start_date"],data["end_date"]])
                        else:
                            reservation_objs = reservation_objs.filter(created_at__gte=data["start_date"])
                cat_id = int(data["filter_category"])
                cat_12 = 0
                if cat_id == 1:
                    reservation_data = reservation_objs.values('patient').annotate(record_count=Count('patient')).filter(record_count=1)
                    cat_12 = 1
                elif cat_id == 2:
                    reservation_data = reservation_objs.values('patient').annotate(record_count=Count('patient')).filter(record_count__gt=1)
                    cat_12=1
                elif cat_id == 3:
                    reservation_objs = reservation_objs.filter(is_accepted=False, scheduled_by__is_patient=True)
                elif cat_id == 4:
                    reservation_objs = reservation_objs.filter(message__isnull=False)
                elif cat_id == 5:
                    reservation_objs = reservation_objs.filter(medication_guidence=True)
                if cat_12:
                    patient_data = []
                    for res_data in reservation_data:
                        patient_data.append(res_data["patient"])
                    reservation_objs = reservation_objs.filter(patient__in=patient_data)
                if "patient" in data:
                    if data["patient"]:
                        reservation_objs = reservation_objs.filter(Q(patient__name__icontains=data["patient"]) | Q(patient__user__email__icontains=data["patient"]))
                return Response(data = ForReservationSearchSerializer(reservation_objs,many=True).data ,status=status.HTTP_200_OK)
            return Response({"message":"予約のデータが見つかりません"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserMemoViewset(viewsets.ModelViewSet):
    """
    CRUD operations of User Memo

    Authentication Required : YES

    Request Data: {
        "pharmacy_name":"",
        "pharmacist":"",
        "memo_scheduled_time" : "2022-06-04",
        "title" :""
        "description":""
    }

    Adding Usermemo to existing Reservation
    
    Request Data: {
        "is_usermemo_added" : True,
        "title" :""
        "description":""
    }

    """
    queryset = UserMemo.objects.all()
    serializer_class = UserMemoSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['id','user__id']
    # pagination_class = None

    def get_queryset(self):
        qs = UserMemo.objects.filter(user=self.request.user).order_by('-updated_at')
        return qs 

    def create(self, request, *args, **kwargs):
        try:
            mutable = request.POST._mutable
            request.POST._mutable = True
            data = request.data
            user_obj = self.request.user
            data["user"] = user_obj.id
            serializer = UserMemoCreateSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response(data = serializer.data ,status=status.HTTP_201_CREATED)
            else:
                return Response(data = serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk):
        try:
            memo_obj = UserMemo.objects.filter(id=pk)
            if memo_obj.count():
                memo_obj = memo_obj.first()
                data = request.data
                serializer = UserMemoCreateSerializer(memo_obj,data=data,partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(data = serializer.data ,status=status.HTTP_202_ACCEPTED)
                else:
                    return Response(data = serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            return Response({"message":"ユーザーメモのデータが見つかりません"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)