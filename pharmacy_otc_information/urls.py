from django.urls import path
from .views import PharmacyOTCInfoViewset, PharmacyOTCSearch, ExportCsvOTCInformation,DrugClassificationAPIView,ExportCsvPharamacyOTCSearch
from rest_framework import routers

router = routers.SimpleRouter()
router.register("pharma_otc_info",PharmacyOTCInfoViewset)
router.register("drug_classification",DrugClassificationAPIView)

urlpatterns = [
    path('pharma_otc/search/',PharmacyOTCSearch.as_view()),
    path('pharma_otc_info/csv/',ExportCsvPharamacyOTCSearch)
] + router.urls