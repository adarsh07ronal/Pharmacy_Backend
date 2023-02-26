
# Create your views here.
from rest_framework import viewsets
from .models import PharmacyOTCInformation, DrugEfficacyClassification
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import HttpResponse
# from rest_framework import status
# Create your views here.
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
import csv,ast
from rest_framework.parsers import MultiPartParser, JSONParser
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from datetime import datetime
from rest_framework.decorators import action
import os
from django.db.models import Q
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination

fs = FileSystemStorage(location='tmp/')

class PharmacyOTCInfoPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'

class PharmacyOTCInfoViewset(viewsets.ModelViewSet):
    """
    CRUD operations for OTC Information

    Authentication Required : YES

    Request Data : {}
    """
 
    queryset = PharmacyOTCInformation.objects.all()
    serializer_class = PharmacyOTCInfoSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['id']
    pagination_class = PharmacyOTCInfoPagination

    parser_classes = [MultiPartParser,JSONParser]

    def list(self, request, *args, **kwargs):
        qs= PharmacyOTCInformation.objects.all().order_by('-updated_at')
        return self.get_paginated_response(PharmacyOTCRetrieveSerializer(self.paginate_queryset(qs),many=True).data)
    
    def retrieve(self, request, pk=None):
        queryset = PharmacyOTCInformation.objects.filter(id=self.kwargs["pk"])
        if queryset.count():
            queryset=queryset.first()
            serializer = PharmacyOTCRetrieveSerializer(queryset)
            return Response(serializer.data)        
        return Response({"message":"薬のデータが見つかりません"},status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['POST'])
    def upload_data(self,request):
        file = request.FILES["file"]

        content = file.read()

        file_content = ContentFile(content)
        file_path = os.path.join('tmp', 'otc_drug_tmp.csv')
        if os.path.exists(file_path):
            os.remove(file_path)
        # os.remove(os.path.join('tmp', 'otc_drug_tmp.csv'))
        file_name = fs.save(
            "otc_drug_tmp.csv", file_content
        )
        
        try:
            tmp_file = fs.path(file_name)
            csv_file = open(tmp_file, errors="ignore")
            reader = csv.reader(csv_file)
            next(reader)
        except:
            return Response("Not a Valid CSV file", status=status.HTTP_400_BAD_REQUEST)
        
        otc_list = []
        for id_, row in enumerate(reader):
            (
                brand_name,
                sales_name_code,
                standard_name,
                japan_standard_prod_classification_number,
                yj_code,
                medicinal_effect_classification_name,
                drug_classification,
                approval_number,
                european_trademark_name,
                nhi_price_standard_listing_date,
                sales_start_date,
                saving_method,
                expiration_date,
                regulation_classification,
                active_ingredient,
                additive,
                properties,
                caveat,
                contraindications,
                contraindications_in_principle,
                efficacy,
                usage_dosage,
                precautions_related_to_usage,
                precautions_for_use,
                important_basic_notes,
                interaction,
                drug_name,
                clinical_symptoms,
                mechanism_riskfactors,
                caution_for_combined_use,
                side_effects,
                other_side_effects,
                administration_to_the_elderly,
                administration_to_pregnant_women,
                administration_to_children,
                overdose,
                precautions_for_application,
                pharmacokinetics,
                pharmacology,
                pharmacological_action,
                physicochemical_knowledge_about_active_ingredients,
                packaging,
                main_documents_and_document_request_destinations,
                document_request_destination,
                information_on_medications_with_limited_dosing_periods,
                name_of_manufacturer_or_distributor
            ) = row

            try:
                nhi_price_standard_listing_date = datetime.strptime(nhi_price_standard_listing_date,'%Y-%m-%d')
                sales_start_date = datetime.strptime(sales_start_date,'%Y-%m-%d')
                expiration_date = datetime.strptime(expiration_date,'%Y-%m-%d')
            except:
                nhi_price_standard_listing_date = datetime.strptime(nhi_price_standard_listing_date,'%Y/%m/%d')
                sales_start_date = datetime.strptime(sales_start_date,'%Y/%m/%d')
                expiration_date = datetime.strptime(expiration_date,'%Y/%m/%d')
            
            nhi_price_standard_listing_date = datetime.strftime(nhi_price_standard_listing_date,"%Y-%m-%d")
            sales_start_date = datetime.strftime(sales_start_date,"%Y-%m-%d")
            expiration_date = datetime.strftime(expiration_date,"%Y-%m-%d")
            
            drug_classification_instances = DrugEfficacyClassification.objects.filter(Q(drug_classification_en__icontains=drug_classification)|Q(drug_classification_jp__icontains=drug_classification))
            if drug_classification_instances.count():
                drug_classification_instance = drug_classification_instances.first()
            else:
                # translator_en= Translator(to_lang="English")
                # translator_jp= Translator(to_lang="Japanese")
                drug_classification_instance =DrugEfficacyClassification.objects.create(drug_classification_en=drug_classification,drug_classification_jp=drug_classification)

            otc_list.append(
                PharmacyOTCInformation(
                    brand_name=brand_name,
                    sales_name_code=sales_name_code,
                    standard_name=standard_name,
                    japan_standard_prod_classification_number=japan_standard_prod_classification_number,
                    yj_code=yj_code,
                    medicinal_effect_classification_name=medicinal_effect_classification_name,
                    drug_classification=drug_classification_instance,
                    approval_number=approval_number,
                    european_trademark_name=european_trademark_name,
                    nhi_price_standard_listing_date=nhi_price_standard_listing_date,
                    sales_start_date=sales_start_date,
                    saving_method=saving_method,
                    expiration_date=expiration_date,
                    regulation_classification=regulation_classification,
                    active_ingredient=active_ingredient,
                    additive=additive,
                    properties=properties,
                    caveat=caveat,
                    contraindications=contraindications,
                    contraindications_in_principle=contraindications_in_principle,
                    efficacy=efficacy,
                    usage_dosage=usage_dosage,
                    precautions_related_to_usage=precautions_related_to_usage,
                    precautions_for_use=precautions_for_use,
                    important_basic_notes=important_basic_notes,
                    interaction=interaction,
                    drug_name=drug_name,
                    clinical_symptoms=clinical_symptoms,
                    mechanism_riskfactors=mechanism_riskfactors,
                    caution_for_combined_use=caution_for_combined_use,
                    side_effects=side_effects,
                    other_side_effects=other_side_effects,
                    administration_to_the_elderly=administration_to_the_elderly,
                    administration_to_pregnant_women=administration_to_pregnant_women,
                    administration_to_children=administration_to_children,
                    overdose=overdose,
                    precautions_for_application=precautions_for_application,
                    pharmacokinetics=pharmacokinetics,
                    pharmacology=pharmacology,
                    pharmacological_action=pharmacological_action,
                    physicochemical_knowledge_about_active_ingredients=physicochemical_knowledge_about_active_ingredients,
                    packaging=packaging,
                    main_documents_and_document_request_destinations=main_documents_and_document_request_destinations,
                    document_request_destination=document_request_destination,
                    information_on_medications_with_limited_dosing_periods=information_on_medications_with_limited_dosing_periods,
                    name_of_manufacturer_or_distributor=name_of_manufacturer_or_distributor
                )
            )
        PharmacyOTCInformation.objects.bulk_create(otc_list)
        return Response("Successfully upload the data",status=status.HTTP_200_OK)

    def update(self, request, *args,**kwargs):
        try:
            mutable = request.POST._mutable
            request.POST._mutable = True
            medicine_obj = PharmacyOTCInformation.objects.filter(id=self.kwargs["pk"])
            if medicine_obj.count():
                medicine_obj = medicine_obj.first()
                data = self.request.data
                if "drug_classification" in data:
                    drug_classification = data["drug_classification"]
                    m_class = DrugEfficacyClassification.objects.filter(Q(drug_classification_en__icontains=drug_classification)|Q(drug_classification_jp__icontains=drug_classification))
                    if m_class.count():
                        m_class = m_class.first()
                    else:
                        m_class = DrugEfficacyClassification.objects.create(drug_classification_en=drug_classification,drug_classification_jp=drug_classification)
                    del data["drug_classification"]
                serializer = PharmacyOTCInfoSerializer(medicine_obj,data=data,partial=True)
                if serializer.is_valid():
                    instance =serializer.save(drug_classification=m_class)
                    return Response(data=PharmacyOTCRetrieveSerializer(instance).data,status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message":"薬のデータが見つかりません"},status=status.HTTP_404_NOT_FOUND)    
        except Exception as e:
            return Response({"message":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ExportCsvOTCInformation(APIView):
    def get(self,request, format=None):
        response = HttpResponse(content_type='text/csv')
        
        writer = csv.writer(response)
        writer.writerow(['brand_name',
                'sales_name_code',
                'standard_name',
                'japan_standard_prod_classification_number',
                'yj_code',
                'medicinal_effect_classification_name',
                'drug_classification',
                'approval_number',
                'european_trademark_name',
                'nhi_price_standard_listing_date',
                'sales_start_date',
                'saving_method',
                'expiration_date',
                'regulation_classification',
                'active_ingredient',
                'additive',
                'properties',
                'caveat',
                'contraindications',
                'contraindications_in_principle',
                'efficacy',
                'usage_dosage',
                'precautions_related_to_usage',
                'precautions_for_use',
                'important_basic_notes',
                'interaction',
                'drug_name',
                'clinical_symptoms',
                'mechanism_riskfactors',
                'caution_for_combined_use',
                'side_effects',
                'other_side_effects',
                'administration_to_the_elderly',
                'administration_to_pregnant_women',
                'administration_to_children',
                'overdose',
                'precautions_for_application',
                'pharmacokinetics',
                'pharmacology',
                'pharmacological_action',
                'physicochemical_knowledge_about_active_ingredients',
                'packaging',
                'main_documents_and_document_request_destinations',
                'document_request_destination',
                'information_on_medications_with_limited_dosing_periods',
                'name_of_manufacturer_or_distributor'])
        
        for obj in PharmacyOTCInformation.objects.all().values_list('brand_name',
                'sales_name_code',
                'standard_name',
                'japan_standard_prod_classification_number',
                'yj_code',
                'medicinal_effect_classification_name',
                'drug_classification',
                'approval_number',
                'european_trademark_name',
                'nhi_price_standard_listing_date',
                'sales_start_date',
                'saving_method',
                'expiration_date',
                'regulation_classification',
                'active_ingredient',
                'additive',
                'properties',
                'caveat',
                'contraindications',
                'contraindications_in_principle',
                'efficacy',
                'usage_dosage',
                'precautions_related_to_usage',
                'precautions_for_use',
                'important_basic_notes',
                'interaction',
                'drug_name',
                'clinical_symptoms',
                'mechanism_riskfactors',
                'caution_for_combined_use',
                'side_effects',
                'other_side_effects',
                'administration_to_the_elderly',
                'administration_to_pregnant_women',
                'administration_to_children',
                'overdose',
                'precautions_for_application',
                'pharmacokinetics',
                'pharmacology',
                'pharmacological_action',
                'physicochemical_knowledge_about_active_ingredients',
                'packaging',
                'main_documents_and_document_request_destinations',
                'document_request_destination',
                'information_on_medications_with_limited_dosing_periods',
                'name_of_manufacturer_or_distributor'):
            writer.writerow(obj)
        response['Content-Disposition'] = 'attachment; filename="otc_info.csv"'
        return response

# class PharmacyOTCDetialView(APIView):
#     def get(self,request,*args,**kwargs):
#         try:
#             pk = self.kwargs['pk']
#             instances = PharmacyOTCDetial.objects.filter(pharma_otc__id=pk)
#             if instances.count():
#                 instance = instances.first()
#                 return Response(data=PharmacyOTCdetailSerializer(instance).data,status=status.HTTP_200_OK)
#             return Response({"message":"No Pharmacy OTC data found"},status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             return Response({"message":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
#     def put(self,request,*args,**kwargs):
#         try:
#             data =self.request.data
#             pk = self.kwargs['pk']
#             instances = PharmacyOTCDetial.objects.filter(pharma_otc__id=pk)
#             if instances.count():
#                 instance = instances.first()
#                 serializer = PharmacyOTCdetailSerializer(instance,data=data,partial=True)
#                 if serializer.is_valid():
#                     serializer.save()
#                     return Response(data=serializer.data,status=status.HTTP_200_OK)
#                 else:
#                     return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
#             return Response({"message":"No Pharmacy OTC data found"},status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             return Response({"message":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class PharmacyOTCSearch(generics.ListAPIView):
    """
    Search functionality for OTC

    Authentication Required : YES

    Required Params : {
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
 
    queryset = PharmacyOTCInformation.objects.all()
    serializer_class = PharmacyOTCInfoSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        get_data = self.request.GET
        if get_data.get('generic_name'):
            generic_name = get_data.get('generic_name')
            if((generic_name is not None) and (generic_name!="")):
                self.queryset = self.queryset.filter(drug_name__icontains=generic_name)
        if get_data.get('effects'):
            effects= self.request.GET.get('effects')
            if((effects is not None) and (effects!="")):
                self.queryset = self.queryset.filter(Q(side_effects__icontains=effects)|Q(other_side_effects__icontains=effects)|Q(efficacy__icontains=effects))
        if get_data.get('drug_efficasy_classification'):
            drug_efficasy_classification = self.request.GET.get('drug_efficasy_classification')
            if((drug_efficasy_classification is not None) and (drug_efficasy_classification!="")):
                self.queryset = self.queryset.filter(Q(drug_classification__drug_classification_en__icontains=drug_efficasy_classification)|Q(drug_classification__drug_classification_jp__icontains=drug_efficasy_classification))
        if get_data.get('warning'):
            warning = self.request.GET.get('warning')
            if((warning is not None) and (warning!="")):
                self.queryset = self.queryset.filter(Q(precautions_related_to_usage__icontains=warning)|Q(precautions_for_use__icontains=warning)|Q(precautions_for_application__icontains=warning)|Q(warning__icontains=warning))
        if get_data.get('inquiry_company_name'):
            inquiry_company_name = self.request.GET.get('inquiry_company_name')
            if((inquiry_company_name is not None) and (inquiry_company_name!="")):
                self.queryset = self.queryset.filter(brand_name__icontains=inquiry_company_name)
        if get_data.get('concomitant'):
            concomitant = self.request.GET.get('concomitant')
            if((concomitant is not None) and (concomitant!="")):
                self.queryset = self.queryset.filter(caution_for_combined_use__icontains=concomitant)
        if get_data.get('contraindications'):
            contraindications = self.request.GET.get('contraindications')
            if((contraindications is not None) and (contraindications!="")):
                self.queryset = self.queryset.filter(Q(contraindications__icontains=contraindications)|Q(contraindications_in_principle__icontains=contraindications))
        if get_data.get('start_update_date'):
            start_update_date = self.request.GET.get('start_update_date')
            if((start_update_date is not None) and (start_update_date!="")):
                self.queryset = self.queryset.filter(updated_at__gte=start_update_date)
        if get_data.get('end_updated_date'):
            end_updated_date = self.request.GET.get('end_updated_date')
            if((end_updated_date is not None) and (end_updated_date!="")):
                self.queryset = self.queryset.filter(updated_at__lte=end_updated_date)        
        return self.queryset

@api_view(('POST',))
@csrf_exempt
def ExportCsvPharamacyOTCSearch(request):
	"""
	OTC Search CSV Export API

	Request Data : {
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
	if request.method=='POST':
		# data = request.data
		data = request.body.decode("utf-8")
		# if type(data) == str:
		data = ast.literal_eval(data)
		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="pharmacy_otc_search_export.csv"'
		writer = csv.writer(response)
		writer.writerow(['brand_name',
                'sales_name_code',
                'standard_name',
                'japan_standard_prod_classification_number',
                'yj_code',
                'medicinal_effect_classification_name',
                'drug_classification',
                'approval_number',
                'european_trademark_name',
                'nhi_price_standard_listing_date',
                'sales_start_date',
                'saving_method',
                'expiration_date',
                'regulation_classification',
                'active_ingredient',
                'additive',
                'properties',
                'caveat',
                'contraindications',
                'contraindications_in_principle',
                'efficacy',
                'usage_dosage',
                'precautions_related_to_usage',
                'precautions_for_use',
                'important_basic_notes',
                'interaction',
                'drug_name',
                'clinical_symptoms',
                'mechanism_riskfactors',
                'caution_for_combined_use',
                'side_effects',
                'other_side_effects',
                'administration_to_the_elderly',
                'administration_to_pregnant_women',
                'administration_to_children',
                'overdose',
                'precautions_for_application',
                'pharmacokinetics',
                'pharmacology',
                'pharmacological_action',
                'physicochemical_knowledge_about_active_ingredients',
                'packaging',
                'main_documents_and_document_request_destinations',
                'document_request_destination',
                'information_on_medications_with_limited_dosing_periods',
                'name_of_manufacturer_or_distributor'])

		instances = PharmacyOTCInformation.objects.all()
		if 'generic_name' in data:
			generic_name = data.get('generic_name')
			if((generic_name is not None) and (generic_name!="")):
				instances = instances.filter(drug_name__icontains=generic_name)
		if 'effects' in data:
			effects= data.get('effects')
			if((effects is not None) and (effects!="")):
				instances = instances.filter(Q(side_effects__icontains=effects)|Q(other_side_effects__icontains=effects)|Q(efficacy__icontains=effects))
		if 'drug_efficasy_classification' in data:
			drug_efficasy_classification = data.get('drug_efficasy_classification')
			if((drug_efficasy_classification is not None) and (drug_efficasy_classification!="")):
				instances = instances.filter(Q(drug_classification__drug_classification_en__icontains=drug_efficasy_classification)|Q(drug_classification__drug_classification_jp__icontains=drug_efficasy_classification))
		if 'warning' in data:
			warning = data.get('warning')
			if((warning is not None) and (warning!="")):
				instances = instances.filter(Q(warning__icontains=warning)|Q(precautions_related_to_usage__icontains=warning)|Q(precautions_for_use__icontains=warning)|Q(precautions_for_application__icontains=warning))
		if 'inquiry_company_name' in data:
			inquiry_company_name = data.get('inquiry_company_name')
			if((inquiry_company_name is not None) and (inquiry_company_name!="")):
				instances = instances.filter(brand_name__icontains=inquiry_company_name)
		if 'concomitant' in data:
			concomitant = data.get('concomitant')
			if((concomitant is not None) and (concomitant!="")):
				instances = instances.filter(caution_for_combined_use__icontains=concomitant)
		if 'contraindications' in data:
			contraindications = data.get('contraindications')
			if((contraindications is not None) and (contraindications!="")):
				instances = instances.filter(Q(contraindications__icontains=contraindications)|Q(contraindications_in_principle__icontains=contraindications))
		if 'start_update_date' in data:
			start_update_date = data.get('start_update_date')
			if((start_update_date is not None) and (start_update_date!="")):
				instances = instances.filter(updated_at__gte=start_update_date)
		if 'end_updated_date' in data:
			end_updated_date = data.get('end_updated_date')
			if((end_updated_date is not None) and (end_updated_date!="")):
				instances = instances.filter(updated_at__lte=end_updated_date)
		for obj in instances.values_list('brand_name',
                'sales_name_code',
                'standard_name',
                'japan_standard_prod_classification_number',
                'yj_code',
                'medicinal_effect_classification_name',
                'drug_classification',
                'approval_number',
                'european_trademark_name',
                'nhi_price_standard_listing_date',
                'sales_start_date',
                'saving_method',
                'expiration_date',
                'regulation_classification',
                'active_ingredient',
                'additive',
                'properties',
                'caveat',
                'contraindications',
                'contraindications_in_principle',
                'efficacy',
                'usage_dosage',
                'precautions_related_to_usage',
                'precautions_for_use',
                'important_basic_notes',
                'interaction',
                'drug_name',
                'clinical_symptoms',
                'mechanism_riskfactors',
                'caution_for_combined_use',
                'side_effects',
                'other_side_effects',
                'administration_to_the_elderly',
                'administration_to_pregnant_women',
                'administration_to_children',
                'overdose',
                'precautions_for_application',
                'pharmacokinetics',
                'pharmacology',
                'pharmacological_action',
                'physicochemical_knowledge_about_active_ingredients',
                'packaging',
                'main_documents_and_document_request_destinations',
                'document_request_destination',
                'information_on_medications_with_limited_dosing_periods',
                'name_of_manufacturer_or_distributor'):
			writer.writerow(obj)
		return response
	else:
		return Response({"message":"GETメソッドが許可されていません"},status=status.HTTP_405_METHOD_NOT_ALLOWED)


class DrugClassificationAPIView(viewsets.ModelViewSet):
    """
    Drug Classification APIView

    Authentication Required : YES
    """

    queryset = DrugEfficacyClassification.objects.all()
    serializer_class = DrugEfficacyClassificationSerializer
    permission_classes = [IsAuthenticated]