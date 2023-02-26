from django.urls import path,include
from notification import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register("notification_api",views.NotificationViewset,basename='notification_api')


urlpatterns = [
    path('', include(router.urls))
]
