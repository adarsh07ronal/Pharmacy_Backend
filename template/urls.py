# from django.urls import path
from .views import TemplateViewset
from rest_framework import routers

router = routers.SimpleRouter()
router.register("template",TemplateViewset)

urlpatterns = [
] + router.urls
