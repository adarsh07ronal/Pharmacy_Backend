from __future__ import unicode_literals

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from django.views.decorators.csrf import csrf_exempt
import csv, ast
from rest_framework.decorators import api_view
from django.shortcuts import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta
from django.db.models import Q
from drug.models import Medicine
from drug.serializers import MedicineSerializer

# Create your views here.

class MedicineViewSet(viewsets.ModelViewSet):
	queryset = Medicine.objects.all().order_by(	'id')
	serializer_class = MedicineSerializer
	filter_backends = [DjangoFilterBackend]
	# filterset_class = MedicineFilter
	filterset_fields=['drug_name','warning','contraindications']

@api_view(('POST',))
@csrf_exempt
def ExportCSVDrugProductAnalysis(request):
	"""
	Drug Product Analysis CSV Export API

	Request Data : {
		"input_date" : "",
		"renew_date" : "",
		"features" : ["drug_classification","medicinal_effect_classification_name","efficacy","warning","contraindications","inquiry_companyname"]
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
			instances = Medicine.objects.filter(Q(created_at__lt=renew_date) & Q(created_at__gt=input_date))
			for instance in instances:
				row_obj=list()
				row_obj.append(instance.id)
				row_obj.append(input_date_o)
				row_obj.append(renew_date_o)
				if "drug_classification" in writer_list:
					row_obj.append(instance.drug_classification.drug_classification_jp)
				if "medicinal_effect_classification_name" in writer_list:
					row_obj.append(instance.medicinal_effect_classification_name)
				if "efficacy" in writer_list:
					row_obj.append(instance.efficacy)
				if "warning" in writer_list:
					row_obj.append(instance.warning)
				if "contraindications" in writer_list:
					row_obj.append(instance.contraindications)
				if "inquiry_companyname" in writer_list:
					row_obj.append(instance.brand_name)
					# row_obj.appen("XXXX")
				if "nameoftheofferer" in writer_list:
					# row_obj.append(instance.numberofsalesbyproduct)
					row_obj.append("XXXX")
				if "salesscore" in writer_list:
					# row_obj.append(instance.productsalesprice)
					row_obj.append("XXXX")
				writer.writerow(row_obj)
			response['Content-Disposition'] = 'attachment; filename="drug_analysis.csv"'
			return response
		else:
			return Response({"message":"更新日を入力してください"},status=status.HTTP_400_BAD_REQUEST)
	else:
		return Response({"message":"GETメソッドが許可されていません"},status=status.HTTP_405_METHOD_NOT_ALLOWED)