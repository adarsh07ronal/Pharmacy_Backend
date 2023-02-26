from django.urls import path, include
from . import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register('drugstore', views.DrugStoreViewSet,basename='drugstore')

urlpatterns = [
	path('',include(router.urls)),
    path('pr_list/',views.PrefecturesListAPI.as_view()),
    path('reservation/drugstore/',views.DrugStoreListAPI.as_view()),
    path('drugstore_info/csv/',views.ExportCsvPharamacy.as_view()),
    path('drugstore/analysis/csv/',views.ExportCSVDrugStoreAnalysis),
    path('pharmacy_info/list/',views.PharmacyInformationListAPI.as_view()),
]