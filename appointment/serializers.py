from rest_framework import serializers

from authentication.models import User
from .models import Appointment


class BookAppointmentSerializer(serializers.ModelSerializer):
    date = serializers.DateField()
    time = serializers.TimeField()
    patient = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    doctor = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(user_type='HEALTH_WORKER'))

    class Meta:
        model = Appointment
        fields = ['date', 'time', 'status', 'patient', 'doctor']


class DoctorAppointmentSerializer(serializers.ModelSerializer):
    date = serializers.DateField()
    time = serializers.TimeField()
    patient = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    doctor = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(user_type='HEALTH_WORKER'))
    status = serializers.ChoiceField(choices=Appointment.STATUS)
    decision = serializers.ChoiceField(choices=Appointment.DECISION_CHOICES, allow_blank=True)

    class Meta:
        model = Appointment
        fields = ['date', 'time', 'status', 'patient', 'doctor', 'decision']

