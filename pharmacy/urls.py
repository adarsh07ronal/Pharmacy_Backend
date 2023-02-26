"""pharmacy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.urls import include
from django.conf import settings
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls import url

schema_view = get_schema_view(
    openapi.Info(
        title="pharmacy API",
        default_version='v1',
        description="pharmacy description",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('admin/', admin.site.urls),
    path('api/', include('article.urls')),
    path('api/', include('drug.urls')),
    path('api/', include('drugstore.urls')),
    path('api/', include('patient.urls')),
    path('api/', include('pharmacy_auth.urls')),
    path('api/', include('notice.urls')),
    path('api/', include('inquiry.urls')),
    path('api/', include('pharmaceutical_manufacturer.urls')),
    # path('api/', include('otc_app.urls')),
    path('api/', include('pharmacy_otc_information.urls')),
    path('api/', include('pharmacy_drug_information.urls')),
    # url('rest-auth/', include('rest_auth.urls')),
    path('accounts/', include('allauth.urls')),
    path('api/', include('reservation.urls')),
    path('api/', include('notification.urls')),
    path('api/', include('message.urls')),
    path('api/', include('medicine_tips.urls')),
    path('api/', include('template.urls')),
    path('api/', include('favorites.urls')),
]

urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns = urlpatterns + [path('silk/', include('silk.urls', namespace='silk'))]
