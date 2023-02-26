from __future__ import unicode_literals
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.views import APIView
from django.contrib.postgres.search import SearchVector, TrigramSimilarity
from rest_framework import status
from .models import DrugStore, Prefecture
from django.shortcuts import get_object_or_404
from .serializers import DrugStoreSerializer, PrefectureSerializer, DrugStoreCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from django.shortcuts import HttpResponse
import csv
from rest_framework.parsers import MultiPartParser, JSONParser
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated
from rest_framework.decorators import action
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
import os, ast
from favorites.models import FavoriteDrugStore
import uuid
from rest_framework.decorators import api_view
from datetime import datetime, timedelta
from itertools import chain
import json

fs = FileSystemStorage(location='tmp/')

User = get_user_model()

class DrugStoreViewSet(viewsets.ModelViewSet):
	"""

	Params (Search) :{
		"prefectures" : "",
		"municipalities":"",
		"drugstore_name":""
	}

	Upload Data: {
		"name" : "",
		"drugstore_name":"",
		"handling_classification":"",
		"address":"",
		"postal_code":"",
		"fax":"",
		"email":"",
		"representative_email":"",
		"business_hours":"",
		"established":"",
		"telephone_number":"",
		"no_of_employee":5
	}

	"""


	queryset = DrugStore.objects.all().order_by('id')
	serializer_class = DrugStoreSerializer
	filter_backends = [DjangoFilterBackend]
	parser_classes = [MultiPartParser,JSONParser]
	# pagination_class = None
	permission_classes = [IsAuthenticatedOrReadOnly]
	filterset_fields = ['id']

	def get_queryset(self):
		get_data = self.request.GET
		queryset = DrugStore.objects.all()
		if "prefectures" in get_data:
			pref_data = get_data["prefectures"]
			qlookup = Q(prefectures__prefecture_name_en=pref_data) | Q(prefectures__prefecture_name_jp=pref_data)
			queryset=queryset.filter(qlookup)
			if queryset.count():
				if "municipalities" in get_data:
					queryset=queryset.filter(address__icontains=get_data["municipalities"])
		if "drugstore_name" in get_data:
			if((get_data["drugstore_name"] is not None) and (get_data["drugstore_name"]!="")):
				# queryset_normal = queryset.filter(drugstore_name__icontains=get_data["drugstore_name"])
				# queryset = queryset.annotate(search=SearchVector('drugstore_name',),).filter(search=get_data["drugstore_name"])
				queryset=queryset.annotate(similarity=TrigramSimilarity('drugstore_name', get_data["drugstore_name"]),).filter(similarity__gt=0.2).order_by('-similarity')
		if "representative" in get_data:
			# queryset=queryset.annotate(search=SearchVector('representative__email',),).filter(search=get_data["representative"])
			queryset=queryset.filter(Q(representative__icontains=get_data["representative"])|Q(user__username__icontains=get_data["representative"])|Q(user__email__icontains=get_data["representative"]))
		return queryset

	# def retrieve(self, request, pk=None):
	# 	queryset = self.queryset
	# 	queryset = get_object_or_404(queryset, pk=pk)
	# 	serializer = (queryset,context={"request": request})
	# 	return Response(serializer.data)
	
	def create(self, request):
		try:
			mutable = request.POST._mutable
			request.POST._mutable = True
			data = self.request.data
			hc_flag=0
			if "user" in data:
				del data["user"]
			if "handling_classification" in data:
				if type(data["handling_classification"]) == str:
					hc = json.loads(str(data["handling_classification"]))
					del data["handling_classification"]
					hc_flag=1
			serializer = DrugStoreCreateSerializer(data=data,partial=True)
			if serializer.is_valid():
				if "email" in data:
					user_obj = User.objects.filter(email=data["email"])
					if user_obj.count():
						user_obj=user_obj.first()
						if DrugStore.objects.filter(user=user_obj).count():
							return Response({"message":"この薬剤師のメールはすでに他の薬局に割り当てられています"},status=status.HTTP_400_BAD_REQUEST)
					else:
						uid = uuid.uuid4()
						if "password" in data:
							password = data["password"]
						else:
							password = uid.hex+"@"
						user_obj = User.objects.create(email=data["email"])
						user_obj.set_password(password)
						user_obj.is_pharmacy=True
						user_obj.is_email_verified=True
						#user_obj.is_verification_updated=True
						user_obj.save()
						user_token, created = Token.objects.get_or_create(user=user_obj)

						html_message = render_to_string('drugstore/drug_store_notification.html', {'creds':{"email":data["email"],"password":password}})
						msg = EmailMultiAlternatives("じぶん薬局の会員登録完了",html_message , data["email"], [data["email"],'karre@eoraa.com'])
						msg.attach_alternative(html_message, "text/html")
						msg.send()
					if hc_flag==1:
						instance = serializer.save(user=user_obj,handling_classification=hc)
					else:	
						instance = serializer.save(user=user_obj)
					return Response(data=DrugStoreSerializer(instance).data,status=status.HTTP_201_CREATED)	
				else:
					return Response({"message":"メールが必要です"},status=status.HTTP_400_BAD_REQUEST)
			else:
				return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
		except Exception as e:
			return Response({"message":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

	def update(self, request, *args,**kwargs):
		try:
			mutable = request.POST._mutable
			request.POST._mutable = True
			data = self.request.data
			if "user" in data:
				del data["user"]
			hc_flag=0
			if "handling_classification" in data:
				if type(data["handling_classification"]) == str:
					hc = json.loads(str(data["handling_classification"]))
					del data["handling_classification"]
					hc_flag=1
			drugstore_instance = DrugStore.objects.filter(id=self.kwargs["pk"])
			if drugstore_instance.count():
				drugstore_instance = drugstore_instance.first()
				serializer = DrugStoreCreateSerializer(drugstore_instance,data=data,partial=True)
				if serializer.is_valid():
					user_obj = drugstore_instance.user
					if "email" in data:
						user_obj = User.objects.filter(email=data["email"])
						if user_obj.count():
							user_obj=user_obj.first()
							if DrugStore.objects.filter(user=user_obj).exclude(id=drugstore_instance.id).distinct().count():
								return Response({"message":"この薬剤師のメールはすでに他の薬局に割り当てられています"},status=status.HTTP_400_BAD_REQUEST)
						else:
							uid = uuid.uuid4()
							password = uid.hex+"@"
							user_obj = User.objects.create(email=data["email"])
							user_obj.set_password(password)
							user_obj.is_pharmacy=True
							user_obj.is_email_verified=True
							#user_obj.is_verification_updated=True
							user_obj.save()
							user_token, created = Token.objects.get_or_create(user=user_obj)

							html_message = render_to_string('drugstore/drug_store_notification.html', {'creds':{"email":data["email"],"password":password}})
							msg = EmailMultiAlternatives("じぶん薬局の会員登録完了",html_message , data["email"], [data["email"],'karre@eoraa.com'])
							msg.attach_alternative(html_message, "text/html")
							msg.send()
					if "password" in data:
						user_obj.set_password(data["password"])
						user_obj.save()
						html_message = render_to_string('drugstore/ds_password_reset.html', {'creds':{"email":data["email"],"password":data["password"]},'instance':drugstore_instance})
						msg = EmailMultiAlternatives("パスワードの再設定が実施されました。",html_message , data["email"], [data["email"],'karre@eoraa.com'])
						msg.attach_alternative(html_message, "text/html")
						msg.send()
					if hc_flag==1:
						instance = serializer.save(user=user_obj,handling_classification=hc)
					else:	
						instance = serializer.save(user=user_obj)
					return Response(data=DrugStoreSerializer(instance).data,status=status.HTTP_202_ACCEPTED)	
				else:
					return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
			else:
				return Response({"message":"ドラッグストアのデータが見つかりません"},status=status.HTTP_404_NOT_FOUND)
		except Exception as e:
			return Response({"message":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
	@action(detail=False, methods=['POST'])
	def upload_data(self,request):
		file = request.FILES["file"]

		content = file.read()

		file_content = ContentFile(content)
		file_path=os.path.join('tmp', 'pharmacy.csv')
		if os.path.exists(file_path):
			os.remove(file_path)
		file_name = fs.save(
			"pharmacy.csv", file_content
		)
		try:
			tmp_file = fs.path(file_name)
			csv_file = open(tmp_file, errors="ignore")
			reader = csv.reader(csv_file)
			next(reader)
		except:
			return Response("Not a Valid CSV file", status=status.HTTP_400_BAD_REQUEST)

		pharmacy_list = []
		for id_, row in enumerate(reader):
			(
				drugstore_name,
				handling_classification,
				address,
				prefecture,
				postal_code,
				fax,
				email,
				representative,
				business_hours,
				established,
				telephone_number,
				no_of_employee
			) = row
			if handling_classification:
				if type(handling_classification) == str:
					handling_classification= ast.literal_eval(handling_classification)
			prefecture_instance = None
			if prefecture:
				p_i = Prefecture.objects.filter(Q(prefecture_name_en__icontains=prefecture)|Q(prefecture_name_jp__icontains=prefecture))
				if p_i.count():
					prefecture_instance = p_i.first()
				else:
					prefecture_instance= Prefecture.objects.create(prefecture_name_en=prefecture,prefecture_name_jp=prefecture)
			if email:
				drug_store = DrugStore.objects.filter(email=email)
				if drug_store.count():
					return Response("{} email has already taken".format(email),status=status.HTTP_406_NOT_ACCEPTABLE)
				user_objs =User.objects.filter(email=email)
				uid = uuid.uuid4()
				if user_objs.count():
					user = user_objs.first()
				else:
					password = uid.hex+"@"
					user = User.objects.create(email=email)
					user.set_password(password)
					user.is_pharmacy=True
					user.is_email_verified=True
					# user.is_verification_updated=True
					user.save()
					user_token, created = Token.objects.get_or_create(user=user)
				pharmacy_list.append(
                    DrugStore(
                        drugstore_name = drugstore_name,
                        handling_classification=handling_classification,
                        address=address,
						user = user,
                        email=email,
						prefectures =prefecture_instance,
						representative=representative,
                        postal_code=postal_code,
                        fax=fax,
                        telephone_number=telephone_number,
                        business_hours=business_hours,
                        established=established,
                        is_linked = False,
						no_of_employee=no_of_employee
                    )
                )
			else:
				return Response("Emails are Manditory",status=status.HTTP_406_NOT_ACCEPTABLE)            
		DrugStore.objects.bulk_create(pharmacy_list)
		return Response("Successfully upload the data",status=status.HTTP_200_OK)
	
class DrugStoreListAPI(APIView):
	"""
	Drug Store Listing API for Reservation/ Favorites

	
	"""
	permission_classes = [IsAuthenticated]

	def get(self,request,*args,**kwargs):
		queryset = DrugStore.objects.all()
		fav_list = list()
		user = self.request.user
		favorites_objs = FavoriteDrugStore.objects.filter(patient__user=user)
		if favorites_objs.count():
			for obj in favorites_objs:
				fav_list.append(obj.drugstore.id)
			fav_queryset=queryset.filter(id__in=fav_list)
			rest_queryset=queryset.exclude(id__in=fav_list)
			queryset = list(chain(fav_queryset,rest_queryset))
		return Response(data=DrugStoreSerializer(queryset,many=True).data, status=status.HTTP_200_OK)

class PrefecturesListAPI(APIView):
	def get(self,request,*args,**kwargs):
		pref_instances = Prefecture.objects.all()
		p_serializer = PrefectureSerializer(pref_instances,many=True)
		# representative_instances = User.objects.filter(is_pharmacy=True)
		# r_serializer = DSUserSerializer(representative_instances,many=True)
		pr_l = {"prefectures":p_serializer.data}
		# ,"representatives" :r_serializer.data}
		return Response(pr_l, status=status.HTTP_200_OK)

class ExportCsvPharamacy(APIView):
	"""
	OTC Search CSV Export API

	Params (Search) :{
		"prefectures" : "",
		"municipalities":"",
		"drugstore_name":""
	}
	"""
	def get(self,request, *args,**kwargs):
		response = HttpResponse(content_type='text/csv')
		writer = csv.writer(response)
		writer.writerow(['drugstore_name','handling_classification','address','postal_code','fax','drugstore_email','representative','business_hours','established','telephone_number','no_of_employee'])

		instances = DrugStore.objects.all()
		get_data = self.request.GET
		if "prefectures" in get_data:
			pref_data = get_data["prefectures"]
			qlookup = Q(prefectures__prefecture_name_en=pref_data) | Q(prefectures__prefecture_name_jp=pref_data)
			instances=instances.filter(qlookup)
			if instances.count():
				if "municipalities" in get_data:
					instances=instances.filter(address__icontains=get_data["municipalities"])
		if "drugstore_name" in get_data:
			if((get_data["drugstore_name"] is not None) and (get_data["drugstore_name"]!="")):
				instances=instances.annotate(similarity=TrigramSimilarity('drugstore_name', get_data["drugstore_name"]),).filter(similarity__gt=0.2).order_by('-similarity')
		if "representative" in get_data:
			instances=instances.filter(Q(representative__icontains=get_data["representative"])|Q(user__username__icontains=get_data["representative"])|Q(user__email__icontains=get_data["representative"]))

		for obj in instances.values_list('drugstore_name','handling_classification','address','postal_code','fax','email','representative','business_hours','established','telephone_number','no_of_employee'):
			writer.writerow(obj)
		response['Content-Disposition'] = 'attachment; filename="drugstore_info_export.csv"'
		return response

@api_view(('POST',))
@csrf_exempt
def ExportCSVDrugStoreAnalysis(request):
	"""
	DrugStore Analysis CSV Export API

	Request Data : {
		"input_date" : "",
		"renew_date" : "",
		"features" : ["handlingclassification","prefectures","municipalities","storename","storetype","numberofsalesbyproduct","productsalesprice"]
	}
	"""
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
			writer_list = ['id','input_date','renew_date'] + features
			print(writer_list)
			writer.writerow(writer_list)
			instances = DrugStore.objects.filter(Q(created_at__lt=renew_date) & Q(created_at__gt=input_date))
			for instance in instances:
				row_obj=list()
				row_obj.append(instance.id)
				row_obj.append(input_date_o)
				row_obj.append(renew_date_o)
				if "handlingclassification" in writer_list:
					row_obj.append(instance.handling_classification)
				if "prefectures" in writer_list:
					if instance.prefectures is not None:
						row_obj.append(instance.prefectures.prefecture_name_jp)
					else:
						row_obj.append("XXXX")
				if "municipalities" in writer_list:
					row_obj.append(instance.municipalities)
				if "storename" in writer_list:
					row_obj.append(instance.drugstore_name)
				if "storetype" in writer_list:
					# row_obj.append(instance.storetype)
					row_obj.append("XXXX")
				if "numberofsalesbyproduct" in writer_list:
					# row_obj.append(instance.numberofsalesbyproduct)
					row_obj.append("XXXX")
				if "productsalesprice" in writer_list:
					# row_obj.append(instance.productsalesprice)
					row_obj.append("XXXX")
				writer.writerow(row_obj)
			response['Content-Disposition'] = 'attachment; filename="drugstore_analysis.csv"'
			return response
		else:
			return Response({"message":"更新日を入力してください"},status=status.HTTP_400_BAD_REQUEST)
	else:
		return Response({"message":"GETメソッドが許可されていません"},status=status.HTTP_405_METHOD_NOT_ALLOWED)

class PharmacyInformationListAPI(APIView):
    def get(self,request, format=None):
        try:
            pharmacy_objs = DrugStore.objects.all()
            if pharmacy_objs.count():
                patient_info_data = {}
                patient_info_data["total_no_of_pharmacies"] = pharmacy_objs.count()
                patient_info_data["service_cooperation_completed"] = pharmacy_objs.filter(is_linked=True).count()
                patient_info_data["not_linked"] = patient_info_data["total_no_of_pharmacies"] - patient_info_data["service_cooperation_completed"]
                patient_info_data["service_utilization"] = (patient_info_data["service_cooperation_completed"]/patient_info_data["total_no_of_pharmacies"])*100
                return Response(data = patient_info_data ,status=status.HTTP_200_OK)
            return Response({"message":"薬局のデータが見つかりません"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)