from django.urls import path, include
from rest_framework import routers
from notice import views

router = routers.DefaultRouter()
router.register('notice_api',views.NoticeViewSet, basename='notice_api')

urlpatterns = [
	path('', include(router.urls)),
    path('notice/create/', views.NoticeCreateAPIView.as_view()),
    path('notice/', views.NoticeListingAPIView.as_view()),
    path('notice/status_delivery_list/', views.NoticeDeliveryAndStatusAPIView.as_view()),
]



