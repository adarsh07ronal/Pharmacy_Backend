from django.urls import path, include
from patient import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('patient_api', views.PatientViewSet,basename='patient_api'),
router.register('patient_insurance_api',views.PatientInsuranceViewSet, basename='patient_insurance_api')
router.register('address_api',views.AddressViewSet, basename='address_api')
router.register('patient_document_api',views.PatientDocumentViewSet, basename='patient_document_api')
router.register('prescription_api',views.PrescriptionViewSet, basename='prescription_api'),
# router.register("prescription_receipt",views.PrescriptionReceiptReservationViewSet,basename='prescription_receipt')
router.register("patient_and_insurence",views.PatientAndPatientInsurenceViewset,basename='patient_and_insurence')


urlpatterns = [
	path('',include(router.urls)),
	path('patient_prescription/<int:pk>/',views.GetPatientPrescriptionApi.as_view(), name='patient_prescription'),
	path('patient_info/csv/',views.ExportCsvPatientInformation.as_view()),
	path('patient_insurance_info/csv/',views.ExportCSVPatientInsuranceInformation),
	path('patient_info/list/',views.PatientInformationListAPI.as_view()),
	path('patient_information/<int:id>/', views.PatientInfoAPIView.as_view()),
	path('calendar/',views.CalendarListingAPI.as_view()),
	path('patient_info/search/',views.PatientInformationSearchAPI.as_view()),
	path('cms/patient_info/search/',views.CMSPatientInformationSearchAPI.as_view()),
	path('drug/search/',views.DrugSearchAPI.as_view()),
	path('drug/classification/',views.ClassificationListAPI.as_view()),
	path('prescription_ocr/',views.OCRPrescriptionFill.as_view()),
]