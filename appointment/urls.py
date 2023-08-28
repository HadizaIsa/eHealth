from django.urls import path
from . import views

urlpatterns = [
    path('', views.BookAppointmentView.as_view(), name='appointment'),
    path('doctor/', views.DoctorAppointmentView.as_view(), name='doctor-appointments'),
    path('doctor/<int:pk>/decision/', views.DoctorDecisionView.as_view(), name='doctor-decision'),
    path('doctor/dashboard/', views.DoctorDashboardView.as_view(), name='doctor-dashboard'),
]
