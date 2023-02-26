from django.urls import path, include
from drug import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register('medicine_api', views.MedicineViewSet,basename='medicine_api')

urlpatterns = [
	path('',include(router.urls)),
    path('drug/analysis/csv/',views.ExportCSVDrugProductAnalysis),
]