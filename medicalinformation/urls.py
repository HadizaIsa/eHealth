from django.urls import path
from . import views

urlpatterns = [
    path('', views.CreateListMedicalInformation.as_view(), name='medical information'),
    path('filter/', views.FilterUsersByMedicalRecordView.as_view(), name='filter-users-by-medical-record'),
    path('all/', views.GetAllMedicalRecords.as_view(), name='users_medical_information'),


]