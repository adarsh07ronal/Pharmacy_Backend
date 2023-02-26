from drugstore.models import DrugStore
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from drug.models import Medicine, MedicineEfficacyClassification
from patient.serializers import *
from patient.models import Patient, PatientInsurance, Address, PatientDocument, Prescription,PrescriptionReceiptReservation
import csv
from django.core.mail import send_mail
from django.shortcuts import HttpResponse
import uuid
import codecs
from paddleocr import PaddleOCR
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from pharmacy_otc_information.models import DrugEfficacyClassification, PharmacyOTCInformation
from reservation.models import ForReservation
from reservation.serializers import ForReservationCalendarSerializer, PrescriptionRetriveAllSerializer
from datetime import datetime, timedelta
from django.db.models import Count
from django.db.models import Q
import os
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
import ast
import codecs
from itertools import chain
from drug.serializers import MedicineRetrieveSerializer
from pharmacy_otc_information.serializers import DrugEfficacyClassificationSerializer, PharmacyOTCRetrieveSerializer
from rest_framework.pagination import PageNumberPagination

fs = FileSystemStorage(location='tmp/')

# Create your views here.

class PatientPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'

class PatientInfoAPIView(APIView):
    """
    Patient Information APIView
    """
    def get(self,request,*args,**kwargs):
        id = self.kwargs["id"]
        qs = Patient.objects.filter(user__id=id)
        if qs.count():
            qs = qs.first()
            return Response(data=PatientInformationSerializer(qs).data,status=status.HTTP_200_OK)
        return Response({"message":"ユーザーのデータが見つかりません"},status=status.HTTP_404_NOT_FOUND)


class PatientViewSet(viewsets.ModelViewSet):
    """
        Patient CRUD operations

        PUT Data : {
            "name" : "",
            "nickname" :"",
            "dob":"2022-05-21T08:19:28.994878Z",
            "phone_no":"",
            "email":"",
            "password":"",
            "gender": "male",
            "address": {
                "id": 7,
                "address": "Address 1",
                "city": "City 1",
                "prefecture": "Prefecture 1",
                "telephone": "852741963"
            },
            "allergy_info":"",
            "allergy_reactive":"",
            "patient_insurance": [
                {
                    "id": 13,
                    "card_choices": 1,
                    "card_image": Upload Image,
                    "expiration_date": "2022-05-21",
                    "date_of_issuance": "2022-05-21",
                    "symbol": "",
                    "date_of_qualification": "2022-05-21",
                    "name_of_head_of_household": null,
                    "insurance_number": "",
                    "recipient_name": "",
                    "insurer_name": "",
                    "insurer_location": "",
                    "underlying_disease": "",
                    "family_medical_institution": "",
                    "family_dispensing_pharmacy": "",
                }
            ]
        }
    """
    
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id','name']
    pagination_class = PatientPagination

    parser_classes = [MultiPartParser,JSONParser]

    @action(detail=False, methods=['POST'])
    def upload_data(self,request):
        file = request.FILES["file"]

        content = file.read()

        file_content = ContentFile(content)
        file_path = os.path.join('tmp', 'patient_tmp.csv')
        if os.path.exists(file_path):
            os.remove(file_path)
        file_name = fs.save(
            "patient_tmp.csv", file_content
        )
        try:
            tmp_file = fs.path(file_name)

            csv_file = open(tmp_file, errors="ignore")
            reader = csv.reader(csv_file)
            next(reader)
        except:
            return Response("Not a Valid CSV file", status=status.HTTP_400_BAD_REQUEST)
        
        patient_list = []
        for id_, row in enumerate(reader):
            (
                name,
                nickname,
                dob,
                phone_no,
                email,
                gender,
                allergy_info,
                allergy_reactive,
                type,
                line_id 
            ) = row
            if line_id=='':
                line_id =None
            if dob =='':
                dob =None
            else:
                try:
                    dob = datetime.strptime(dob,'%Y-%m-%d')
                except:           
                    dob = datetime.strptime(dob,'%Y/%m/%d')
                dob = datetime.strftime(dob, "%Y-%m-%d")
            p_f = 0
            if email:
                patient_objs = Patient.objects.all()
                if patient_objs.filter(email=email).count():
                    p_f=1
                user_objs =User.objects.filter(email=email)
                if user_objs.count():
                    user = user_objs.first()
                    if patient_objs.filter(user=user).count():
                        p_f = 1    
                else:
                    uid = uuid.uuid4()
                    password = uid.hex+"@"
                    user = User.objects.create(email=email)
                    user.set_password(password)
                    user.is_patient=True
                    user.is_email_verified=True                    
                    user.is_import_creation=True
                    user.save()
                    user_token, created = Token.objects.get_or_create(user=user)
                    send_mail(
                        'じぶん薬局の会員登録認証',
                        "じぶん薬局運営事務局です。\nこの度は、会員登録申請をありがとうございます。\n\nログイン情報 \nメールアドレス：{}\nパスワード：{}\n\nまた、本メールに関するお問い合わせは運営事務局までお願いいたします。\n\n////////////\nじぶん薬局運営事務局\n住所：〒254-0014\n神奈川県平塚市四之宮1-4-13\nE-mail：info@orthros.com".format(email,password),
                        'developers.geitpl@gmail.com',
                        [email,'karre@eoraa.com'],
                    )
                if p_f ==0:
                    patient_list.append(
                        Patient(
                            name=name,
                            user = user,
                            nickname=nickname,
                            dob=dob,
                            phone_no=phone_no,
                            email=email,
                            gender=gender,
                            allergy_info=allergy_info,
                            allergy_reactive=allergy_reactive,
                            type=type,
                            line_id=line_id,
                            is_linked = False
                        )
                    )
            else:
                return Response("Email is Manditory",status=status.HTTP_406_NOT_ACCEPTABLE)            
        patients = Patient.objects.bulk_create(patient_list)
        print(patients)
        if self.request.user.is_pharmacy:
            pharmacy= DrugStore.objects.filter(user=self.request.user)
            if pharmacy.count():
                pharmacy = pharmacy.first()
                for patient in patients:
                    patient.pharmacy_visited.add(pharmacy.id)
                    # patient.save()
        return Response("Successfully upload the data",status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'])
    def upload_data_with_validation(self, request):
        """Upload data from CSV, with validation."""
        file = request.FILES.get("file")

        try:
            reader = csv.DictReader(codecs.iterdecode(file, "utf-8"), delimiter=",")
        except:
            return Response("Not a Valid CSV file")
        data = list(reader)

        serializer = self.serializer_class(data=data, many=True)
        serializer.is_valid(raise_exception=True)

        patient_list = []
        for row in serializer.data:
            patient_list.append(
                Patient(
                    name=row["name"],
                    nickname=row["nickname"],
                    dob=row["dob"],
                    email=row["email"],
                    phone_no=row["phone_no"],
                    gender=row["gender"],
                    allergy_info=row["allergy_info"],
                    allergy_reactive=row["allergy_reactive"],
                    type=row["type"],
                    line_id=row["line_id"]
                )
            )

        Patient.objects.bulk_create(patient_list)

        return Response("Successfully upload the data")

    def update(self, request, *args,**kwargs):
        try:
            mutable = request.POST._mutable
            request.POST._mutable = True
            data = self.request.data
            patient_instance = Patient.objects.filter(id=self.kwargs["pk"])
            if patient_instance.count():
                patient_instance = patient_instance.first()
                if "name" in data:
                    user_obj = patient_instance.user
                    user_obj.username = data["name"] 
                    user_obj.save()
                if "password" in data:
                    special_characters = """!@#$%^&*()-+?_=,<>/"""
                    password = data["password"]
                    if any(i in special_characters for i in password) and any(char.isalpha() for char in password) and any(char.isdigit() for char in password):
                        user_obj = patient_instance.user
                        email = patient_instance.email
                        if user_obj:
                            pass
                        else:
                            if "email" in data:
                                email= data["email"]
                            user_obj = User.objects.create(email=email,is_patient=True)
                        user_obj.set_password(password)
                        user_obj.save()
                        send_mail(
                            'User Credentials',
                            "Please check the details below\nEmail: {}\nPassword: {}\n\nYou can access the portal through\n{}".format(email,password,"https://pharmacy-user.netlify.app/"),
                            'developers.geitpl@gmail.com',
                            [email,'karre@eoraa.com'],
                        )
                        user_token, created = Token.objects.get_or_create(user=user_obj)
                    else:
                        return Response({"password":"パスワードは半角英数でご入力ください"}, status=status.HTTP_400_BAD_REQUEST)
                    del data["password"]
                if "patient_insurance" in data:
                    patient_ins_objs = ast.literal_eval(data["patient_insurance"])
                    for patient_ins_obj in patient_ins_objs:
                        obj_flag = 0
                        if "id" in patient_ins_obj:
                            objs = PatientInsurance.objects.filter(id=patient_ins_obj["id"])
                            if objs.count():
                                obj = objs.first()
                                obj_flag = 1
                        else:
                            obj = PatientInsurance.objects.create(card_choices=patient_ins_obj["card_choices"])
                            del patient_ins_obj["card_choices"]
                            obj_flag = 1
                        if obj_flag == 1:
                            serializer = PatientInsuranceSerializer(obj,data=patient_ins_obj,partial=True)
                            if serializer.is_valid():
                                serializer.save(patient=patient_instance)
                            else:
                                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
                    del data["patient_insurance"]
                if "address" in data:
                    add_flag = 1
                    address_obj = ast.literal_eval(data["address"])
                    if "id" in address_obj:
                        address_instance = Address.objects.filter(id=address_obj["id"])
                        if address_instance.count():
                            address_instance = address_instance.first()
                            add_flag = 1
                    else:
                        address_instance = Address.objects.create(patient=patient_instance,address=address_obj["address"],city=address_obj["city"])
                        del address_obj["address"]
                        del address_obj["city"]
                        add_flag = 1
                    if add_flag == 1:
                        serializer = AddressSerializer(address_instance,data=address_obj,partial=True)
                        if serializer.is_valid():
                            serializer.save()    
                        else:
                            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
                        del data["address"]
                serializer = PatientSerializer(patient_instance,data=data,partial=True)
                if serializer.is_valid():
                    instance = serializer.save()
                    return Response(data=PatientInformationSerializer(instance).data,status=status.HTTP_200_OK)    
                else:
                    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            return Response({"message":"患者のデータが見つかりません"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def retrieve(self, request, pk=None):
        queryset = Patient.objects.filter(id=self.kwargs["pk"])
        if queryset.count():
            queryset=queryset.first()
            serializer = PatientInformationPharmacySerializer(queryset)
            return Response(serializer.data)        
        return Response({"message":"患者のデータが見つかりません"},status=status.HTTP_404_NOT_FOUND)
    
    def list(self, request):
        queryset = Patient.objects.all()
        if "pharmacy" in self.request.GET:
            if self.request.GET["pharmacy"]:
                queryset = Patient.objects.filter(pharmacy_visited__in=[self.request.GET["pharmacy"]])
                # reservation_objs = ForReservation.objects.filter(pharmacy=self.request.GET["pharmacy"])
                # if reservation_objs.count():
                #     reservation_data = reservation_objs.values('patient').annotate(record_count=Count('patient'))
                #     patient_data = []
                #     for res_data in reservation_data:
                #         patient_data.append(res_data["patient"])
                #     if patient_data:
                #         queryset = queryset.filter(id__in=patient_data)
        if queryset.count():
            # serializer = PatientSerializer(queryset,many=True)
            # return Response(serializer.data)        
            return self.get_paginated_response(PatientSerializer(self.paginate_queryset(queryset),many=True).data)
        return Response({"message":"患者のデータが見つかりません"},status=status.HTTP_404_NOT_FOUND)

class PatientInsuranceViewSet(viewsets.ModelViewSet):
	queryset = PatientInsurance.objects.all()
	serializer_class = PatientInsuranceSerializer
	parser_classes = (MultiPartParser,)
	

class AddressViewSet(viewsets.ModelViewSet):
	queryset = Address.objects.all()
	serializer_class = AddressSerializer


class PatientDocumentViewSet(viewsets.ModelViewSet):

	queryset = PatientDocument.objects.all()
	serializer_class = PatientDocumentSerializer
	# parser_classes = (MultiPartParser,)
	# def perform_create(self,serializer):

		
class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    parser_classes = (MultiPartParser,)
    
    def create(self,request):
        # special_characters = """!@#$%^&*()-+?_=,<>/"""
        data = request.data
        # insurer_number = data.get('insurer_number')
        user_details = self.request.user
        if "patient" in data:
            del data["patient"]
        # if any(char.isalpha() for char in insurer_number) and any(char.isdigit() for char in insurer_number):
        serializer = PrescriptionSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save(patient=Patient.objects.get(user=user_details))
        return Response(PrescriptionCreateRetriveSerializer(obj).data)
        # else:
        #     return Response({"insurer_number":"please enter the insurer_number in half-width alphanumeric characters"}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        qs= Prescription.objects.filter(patient__user=self.request.user)
        return Response(PrescriptionRetriveSerializer(qs,many=True).data)
    
    def retrieve(self, request, *args, **kwargs):
        qs= Prescription.objects.filter(id=self.kwargs["pk"])
        if qs.count():
            qs = qs.first()
            return Response(PrescriptionRetriveAllSerializer(qs).data)
        else:
            return Response({"message":"処方データが見つかりません"})

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

class GetPatientPrescriptionApi(APIView):
	serializer_class = PrescriptionSerializer
	def get(self,request,pk):
		try:
			patient_obj = Patient.objects.get(id=pk)
		except:
			return Response({"patient":"patient is not in the list"}, status=status.HTTP_400_BAD_REQUEST)
		prescription_obj = Prescription.objects.filter(patient=patient_obj)
		serializer = PrescriptionSerializer(prescription_obj, many=True)
		return Response(serializer.data)		

class PrescriptionReceiptReservationViewSet(viewsets.ModelViewSet):
	queryset = PrescriptionReceiptReservation.objects.all()
	serializer_class = PrescriptionReceiptReservationSerializer

class PatientAndPatientInsurenceViewset(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientAndPatientInsurenceSerializer

    def get_serializer_context(self):
        context = super(PatientAndPatientInsurenceViewset, self).get_serializer_context()
        if "patient_insurance" in self.request.data:
            context.update({"insurance_data": self.request.data["patient_insurance"]})
        return context
	
class ExportCsvPatientInformation(APIView):
    def get(self,request, format=None):
        response = HttpResponse(content_type='text/csv')
        
        writer = csv.writer(response)
        writer.writerow(['name',
                'nickname',
                'dob',
                'phone_no',
                'email',
                'gender',
                'allergy_info',
                'allergy_reactive',
                'type',
                'line_id'])
        
        for obj in Patient.objects.all().values_list('name','nickname','dob','phone_no','email','gender','allergy_info','allergy_reactive','type','line_id'):
            writer.writerow(obj)
        response['Content-Disposition'] = 'attachment; filename="patient_info.csv"'
        return response

class PatientInformationListAPI(APIView):
    def get(self,request, format=None):
        try:
            patient_objs = Patient.objects.all()
            if patient_objs.count():
                patient_info_data = {}
                patient_info_data["total_no_of_patients"] = patient_objs.count()
                patient_info_data["service_cooperation_completed"] = patient_objs.filter(is_linked=True).count()
                patient_info_data["not_linked"] = patient_info_data["total_no_of_patients"] - patient_info_data["service_cooperation_completed"]
                patient_info_data["service_utilization"] = (patient_info_data["service_cooperation_completed"]/patient_info_data["total_no_of_patients"])*100
                return Response(data = patient_info_data ,status=status.HTTP_200_OK)
            return Response({"message":"患者のデータが見つかりません"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CalendarListingAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request, *args, **kwargs):
        try:
            patient_objs = Patient.objects.filter(user = self.request.user)
            if patient_objs.count():
                patient_obj = patient_objs.first()
                calendar_data = []
                reservation_objs = ForReservation.objects.filter(patient=patient_obj)
                if reservation_objs.count():
                    for res in reservation_objs:
                        reservation_data={"reservation_date":None,"remote_guidance_date":None}
                        res_flg = 0
                        rem_guid_flg = 0
                        if res.is_accepted:
                            reservation_data["reservation_date"] = res.reservation_scheduled_time 
                            res_flg = 1
                        if res.is_remote_accepted:
                            reservation_data["remote_guidance_date"] = res.guidance_scheduled_time
                            rem_guid_flg = 1
                        if res_flg or rem_guid_flg:
                            reservation_data["reservation_details"] = ForReservationCalendarSerializer(res).data
                            reservation_data["prescription_details"] = PrescriptionCalenderSerializer(res.prescription,many=True).data
                            calendar_data.append(reservation_data)
                    return Response(data = calendar_data ,status=status.HTTP_200_OK)
                return Response({"message":"Patient has no Reservation data"},status=status.HTTP_404_NOT_FOUND)    
            return Response({"message":"No Calendar data found"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PatientInformationSearchAPI(APIView):
    """
    Patient Information Search API

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
            patient_objs = Patient.objects.all()
            if "start_date" in data:
                if data["start_date"]:
                    if "end_date" in data:
                        if data["end_date"]:
                            patient_objs = patient_objs.filter(created_at__range=[data["start_date"],data["end_date"]])
                    else:
                        patient_objs = patient_objs.filter(created_at__gte=data["start_date"])
            if "patient" in data:
                if data["patient"]:
                    patient_objs = patient_objs.filter(Q(name__icontains=data["patient"]) | Q(user__email__icontains=data["patient"]))
            
            if "filter_category" in data:
                reservation_objs = ForReservation.objects.filter(pharmacy__user=self.request.user)
                cat_id = int(data["filter_category"])
                if cat_id == 1:
                    reservation_data = reservation_objs.values('patient').annotate(record_count=Count('patient')).filter(record_count=1)
                elif cat_id == 2:
                    reservation_data = reservation_objs.values('patient').annotate(record_count=Count('patient')).filter(record_count__gt=1)
                elif cat_id == 3:
                    reservation_data = reservation_objs.values('patient').filter(is_accepted=False, scheduled_by__is_patient=True)
                elif cat_id == 4:
                    reservation_data = reservation_objs.values('patient').filter(message__isnull=False)
                elif cat_id == 5:
                    reservation_data = reservation_objs.values('patient').filter(medication_guidence=True)
                patient_data = []
                for res_data in reservation_data:
                    patient_data.append(res_data["patient"])
                patient_objs = patient_objs.filter(id__in=patient_data)
            
            return Response(data = PatientSerializer(patient_objs,many=True).data ,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CMSPatientInformationSearchAPI(APIView):
    """
    CMS Patient Information Search API

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
            patient_objs = Patient.objects.all()
            if patient_objs.count():
                if "start_date" in data:
                    if data["start_date"]:
                        if "end_date" in data:
                            if data["end_date"]:
                                patient_objs = patient_objs.filter(created_at__range=[data["start_date"],data["end_date"]])
                        else:
                            patient_objs = patient_objs.filter(created_at__gte=data["start_date"])
                
                if "patient" in data:
                    if data["patient"]:
                        patient_objs = patient_objs.filter(Q(name__icontains=data["patient"]) | Q(user__email__icontains=data["patient"]))
                # if "filter_category" in data:
                #     patient_objs = patient_objs.filter(is_linked=True)
                if "filter_category" in data:
                    if data["filter_category"]==1:
                        patient_objs = patient_objs.filter(is_linked=True)
                    elif data["filter_category"]==2:
                        patient_objs = patient_objs.filter(is_linked=False)
                return Response(data = PatientCMSInfoSearchSerializer(patient_objs,many=True).data ,status=status.HTTP_200_OK)
            return Response({"message":"患者のデータが見つかりません"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(('POST',))
@csrf_exempt
def ExportCSVPatientInsuranceInformation(request):
    """
    Patient Insurance CSV Export API

    Request Data : {
        "input_date" : "",
        "renew_date" : "",
        "features" : ["gender","patient_address","allergy_reactive","allergy_info","underlying_disease","family_medical_institution","family_dispensing_pharmacy","insurance_card_name","insurance_name","insurance_number","office_name"]
    }
    """

    # def get(self,request, *args,**kwargs):
    if request.method=='POST':
        data = request.body.decode("utf-8")
        data = ast.literal_eval(data)
        if ("input_date" in data) and ("renew_date" in data):
            input_date_o = data["input_date"]
            renew_date_o = data["renew_date"]
            response = HttpResponse(content_type='text/csv')
            td = timedelta(1)
            try:
                input_date = datetime.strptime(input_date_o,'%Y-%m-%d') - td
                renew_date = datetime.strptime(renew_date_o,'%Y-%m-%d') + td
            except:           
                input_date = datetime.strptime(input_date_o,'%Y/%m/%d') - td
                renew_date = datetime.strptime(renew_date_o,'%Y/%m/%d') + td
            input_date = datetime.strftime(input_date, "%Y-%m-%d")
            renew_date = datetime.strftime(renew_date, "%Y-%m-%d")
            writer = csv.writer(response)
            features = data["features"]
            if type(features)==str:
                features = ast.literal_eval(features)
            writer_list = ['input_date','renew_date'] + features
            writer.writerow(writer_list)
            
            instances = Patient.objects.filter(Q(created_at__lt=renew_date) & Q(created_at__gt=input_date))
            for instance in instances:
                try:
                    address_obj = instance.address
                except:
                    address_obj = None
                if (("underlying_disease" in writer_list) or ("family_medical_institution" in writer_list) or ("family_dispensing_pharmacy" in writer_list) or ("insurance_card_name" in writer_list) or ("insurance_name" in writer_list) or ("insurance_number" in writer_list) or ("office_name" in writer_list)):
                    insurance_objs = instance.patient_insurance.all()
                    for obj in insurance_objs:
                        row_obj=list()
                        # row_obj.append(obj.id)
                        row_obj.append(input_date_o)
                        row_obj.append(renew_date_o)
                        if "gender" in writer_list:
                            row_obj.append(instance.gender)
                        if "patient_address" in writer_list:
                            if address_obj:
                                row_obj.append(address_obj.address)
                            else:
                                row_obj.append("xxxxxxx")
                        if "allergy_reactive" in writer_list:
                            row_obj.append(instance.allergy_reactive)
                        if "allergy_info" in writer_list:
                            row_obj.append(instance.allergy_info)
                        if "underlying_disease" in writer_list:
                            row_obj.append(obj.underlying_disease)
                        if "family_medical_institution" in writer_list:
                            row_obj.append(obj.family_medical_institution)
                        if "family_dispensing_pharmacy" in writer_list:
                            row_obj.append(obj.family_dispensing_pharmacy)
                        if "insurance_card_name" in writer_list:
                            if obj.card_choices==1:
                                row_obj.append("Business health insurance card")
                            else:
                                row_obj.append("National health insurance card")
                        if "insurance_name" in writer_list:
                            row_obj.append(obj.insurer_name)
                        if "insurance_number" in writer_list:
                            row_obj.append(obj.insurance_number)
                        if "office_name" in writer_list:
                            row_obj.append(obj.office_name)
                        writer.writerow(row_obj)
                else:
                    patient_row_obj = list()
                    patient_row_obj.append(input_date_o)
                    patient_row_obj.append(renew_date_o)
                    if "gender" in writer_list:
                        patient_row_obj.append(instance.gender)
                    if "patient_address" in writer_list:
                        if address_obj:
                            patient_row_obj.append(address_obj.address)
                        else:
                            patient_row_obj.append("xxxxxxx")
                    if "allergy_reactive" in writer_list:
                        patient_row_obj.append(instance.allergy_reactive)
                    if "allergy_info" in writer_list:
                        patient_row_obj.append(instance.allergy_info)
                    writer.writerow(patient_row_obj)
            response['Content-Disposition'] = 'attachment; filename="patient_insurance_info.csv"'
            return response
        else:
            return Response({"message":"更新日を入力してください"},status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"message":"GETメソッドが許可されていません"},status=status.HTTP_405_METHOD_NOT_ALLOWED)

class ClassificationListAPI(APIView):
    """
    List of Drug classifications

    Authentication Required : NO
    """    

    def get(self,request,*args,**kwargs):
        otcclass_ins = DrugEfficacyClassification.objects.all()
        drugclass_ins = MedicineEfficacyClassification.objects.all()
        result_list = list(chain(drugclass_ins, otcclass_ins))
        otclass_serializer = DrugEfficacyClassificationSerializer(result_list,many=True)
        return Response(data=otclass_serializer.data, status=status.HTTP_200_OK)

class DrugSearchAPI(APIView):
    """
    Search functionality for Drugs (OTC/Prescribed)

    Authentication Required : YES

    Required Params : {
        "search_classification" : 1/2 (Manditory),
        "generic_name":"",
        "effects":"",
        "drug_efficasy_classification":"",
        "warning":"",
        "inquiry_company_name":"",
        "concomitant":"",
        "contraindications":"",
        "start_update_date":"",
        "end_updated_date":"",
    }
    """
    permission_classes = [IsAuthenticated]

    def get(self,request,*args,**kwargs):
        try:
            get_data = self.request.GET
            search_classification = 1
            queryset = []
            if 'search_classification' in get_data:
                search_classification=int(get_data.get('search_classification'))
                if search_classification==1:
                    queryset = PharmacyOTCInformation.objects.all()
                else:
                    queryset = Medicine.objects.all()
                # queryset = list(chain(otc_queryset, drug_queryset))
                if queryset.count():
                    if 'generic_name' in get_data:
                        generic_name = get_data.get('generic_name')
                        if((generic_name is not None) and (generic_name!="")):
                            queryset = queryset.filter(drug_name__icontains=generic_name)
                    if 'effects' in get_data:
                        effects= self.request.GET.get('effects')
                        if((effects is not None) and (effects!="")):
                            queryset = queryset.filter(Q(side_effects__icontains=effects)|Q(other_side_effects__icontains=effects)|Q(efficacy__icontains=effects))
                    if 'drug_efficasy_classification' in get_data:
                        drug_efficasy_classification = self.request.GET.get('drug_efficasy_classification')
                        if((drug_efficasy_classification is not None) and (drug_efficasy_classification!="")):
                            queryset = queryset.filter(Q(drug_classification__drug_classification_en__icontains=drug_efficasy_classification)|Q(drug_classification__drug_classification_jp__icontains=drug_efficasy_classification))
                    if 'warning' in get_data:
                        warning = self.request.GET.get('warning')
                        if((warning is not None) and (warning!="")):
                            queryset = queryset.filter(Q(precautions_related_to_usage__icontains=warning)|Q(warning__icontains=warning)|Q(precautions_for_use__icontains=warning)|Q(precautions_for_application__icontains=warning))
                    if 'inquiry_company_name' in get_data:
                        inquiry_company_name = self.request.GET.get('inquiry_company_name')
                        if((inquiry_company_name is not None) and (inquiry_company_name!="")):
                            queryset = queryset.filter(brand_name__icontains=inquiry_company_name)
                    if 'concomitant' in get_data:
                        concomitant = self.request.GET.get('concomitant')
                        if((concomitant is not None) and (concomitant!="")):
                            queryset = queryset.filter(caution_for_combined_use__icontains=concomitant)
                    if 'contraindications' in get_data:
                        contraindications = self.request.GET.get('contraindications')
                        if((contraindications is not None) and (contraindications!="")):
                            queryset = queryset.filter(Q(contraindications__icontains=contraindications)|Q(contraindications_in_principle__icontains=contraindications))
                    if 'start_update_date' in get_data:
                        start_update_date = self.request.GET.get('start_update_date')
                        if((start_update_date is not None) and (start_update_date!="")):
                            queryset = queryset.filter(updated_at__gte=start_update_date)
                    if 'end_updated_date' in get_data:
                        end_updated_date = self.request.GET.get('end_updated_date')
                        if((end_updated_date is not None) and (end_updated_date!="")):
                            queryset = queryset.filter(updated_at__lte=end_updated_date)        
                    if search_classification==1:
                        return Response(PharmacyOTCRetrieveSerializer(queryset,many=True).data,status=status.HTTP_200_OK)
                    else:
                        return Response(MedicineRetrieveSerializer(queryset,many=True).data,status=status.HTTP_200_OK)
                return Response({"message": "薬のデータが見つかりません"},status=status.HTTP_200_OK)
            return Response({"message": "検索分類は必須です"},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class OCRPrescriptionFill(APIView):
    
    parser_classes = [MultiPartParser,JSONParser]

    def post(self,request,*args,**kwargs):
        file = request.FILES["file"]

        content = file.read()

        file_content = ContentFile(content)
        file_path = os.path.join('tmp', '_tmp.png')
        if os.path.exists(file_path):
            os.remove(file_path)
        file_name = fs.save(
            "_tmp.png", file_content
        )

        try:
            tmp_file = fs.path(file_name)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)        
        # ocr = PaddleOCR(use_angle_cls=True, lang='japan') # need to run only once to download and load model into memory
        # img_path = tmp_file
        # result = ocr.ocr(img_path, cls=True)
        # data = list()
        # if result:
        #     for i in range(0,len(result)):
        #         data.append(result[i][1][0])
        data = {
            "prescription_date": "2022-09-01",
            "insurer_number": "煉獄12",
            "name": "煉獄12" ,
            "birthday": "2000-09-01",
            "medical_institution_name": "煉獄12",
            "contact": "煉獄12",
            "prescribing_physician": "煉獄12",
            "prescription_details": "煉獄12煉獄12vvvvv煉獄12"
        }

        

        return Response(data)