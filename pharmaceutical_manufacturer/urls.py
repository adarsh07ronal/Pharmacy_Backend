from django.urls import path, include
from . import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register('pharma_manf', views.PharmaceuticalManufacturerViewset)
router.register('advertisement_list', views.AdvertisementListingViewset)
# router.register('advertising_status', views.AdvertisingStatusViewset)

urlpatterns = [
	path('',include(router.urls)),
	path('clickscounter/',views.ClicksCounterAPIView.as_view()),
	path('pp_list/',views.PPListAPI.as_view()),
]