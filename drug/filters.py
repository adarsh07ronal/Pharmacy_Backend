from django.db.models import Q
from django_filters import rest_framework as filters 

from drug.models import Medicine
import django_filters

class MedicineFilter(django_filters.FilterSet):
	drug_class_name = filters.CharFilter(method='filter_drug')
	search = filters.CharFilter(method='filter_search')

	class Meta:
		model = Medicine
		fields = ['drug_class_name',]

	def filter_drug(self, queryset, name,value):
		if value:
			queryset = queryset.filter(drug_class_name=value)
		return queryset

	def filter_search(self, queryset, name, value):
		if value:
			queryset = queryset.filter(Q(drug_class_name__icontains = value)|Q(sales_name__icontains = value))
		return queryset