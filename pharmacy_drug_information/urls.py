from django.urls import path
from .views import PharmacyDrugInfoViewset,ExportCsvDrugInformation,PharmacyDrugSearch,OCRDrugSearch,OCRDrugFill,ExportCsvPharamacyDrugSearch
from rest_framework import routers

router = routers.SimpleRouter()
router.register("pharma_drug_info",PharmacyDrugInfoViewset)

urlpatterns = [
    path('drug_ocr/search/',OCRDrugSearch.as_view()),
    path('drug_ocr/',OCRDrugFill.as_view()),
    path('pharma_drug_info/search/',PharmacyDrugSearch.as_view()),
    path('pharma_drug_info/csv/',ExportCsvPharamacyDrugSearch)
] + router.urls