from django.urls import path, include
from rest_framework import routers
from inquiry import views

router = routers.DefaultRouter()
router.register('inquiry_api',views.InquiryViewSet, basename='inquiry_api'),


urlpatterns = [
	path('', include(router.urls)),
	path('inquiry/<int:id>/', views.RegisteredInquiryAPIView.as_view()),
	path('inquiry/reply/<int:id>/', views.RegisteredInquiryCreateAPIView.as_view()),
]

