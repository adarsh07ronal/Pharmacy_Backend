from django.urls import path, include
from rest_framework import routers
from article import views

router = routers.DefaultRouter()

router.register('article_api', views.ArticleViewSet, basename='article_api')

urlpatterns = [
	path('', include(router.urls)),
	]

