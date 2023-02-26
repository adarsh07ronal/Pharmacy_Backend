from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('medicine_tips',views.MedicineTipsViewSet, basename='medicine_tips')
router.register('medicine_tips_category',views.MedicineTipsCategoryViewset, basename='medicine_tips_category')

urlpatterns = [
	path('', include(router.urls))
]