from django.urls import path
from . import views

urlpatterns = [
    path('favorite/drugstore/',views.DrugStoreFavoriteAPIView.as_view()),
]