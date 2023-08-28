from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="eHealth API",
      default_version='v1',
      description="an api for managing medical information and appointments",
      terms_of_service="https://www.google.com/policies/terms/",
      incontact=openapi.Contact(email="hadeezah18@gmail.com"),

   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('medicalinfo/', include('medicalinformation.urls')),
    path('appointment/', include('appointment.urls')),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema_json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc')
]
