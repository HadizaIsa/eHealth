from django.utils import timezone

from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Appointment
from django.core.mail import send_mail

from . import serializers

User = get_user_model()


# Create your views here.
class BookAppointmentView(generics.ListCreateAPIView):
    serializer_class = serializers.BookAppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        appointments = Appointment.objects.all()
        return appointments

    def perform_create(self, serializer):
        user = self.request.user
        doctor = serializer.validated_data['doctor']
        date = serializer.validated_data['date']
        time = serializer.validated_data['time']

        # Create the appointment
        appointment = Appointment.objects.create(
            patient=user,
            doctor=doctor,
            date=date,
            time=time,
            status='PENDING'
        )

        # Send confirmation email to patient and health worker
        send_mail(
            'Appointment Confirmation',
            f'You have successfully booked an appointment with {doctor.fullname} on {date} at {time}.',
            'from@ehealth.com',
            [user.email, doctor.email],
            fail_silently=False,
        )
        return Response({'message': 'Appointment booked successfully.'}, status=status.HTTP_201_CREATED)

        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DoctorAppointmentView(generics.ListAPIView):
    serializer_class = serializers.BookAppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.user_type == 'HEALTH_WORKER':
            return Appointment.objects.filter(doctor=user)

        return Appointment.objects.none()


class DoctorDecisionView(generics.UpdateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = serializers.DoctorAppointmentSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        doctor = self.request.user
        patient = serializer.validated_data['patient']
        date = serializer.validated_data['date']
        time = serializer.validated_data['time']

        # Handle decision updates
        decision = serializer.validated_data.get('decision')

        # Handle logic based on status and decision
        if status == 'PENDING' and decision == 'ACCEPTED':
            send_mail(
                'Appointment Confirmation',
                f'Your appointment has been confirmed with {doctor.fullname} on {date} at {time}.',
                'from@ehealth.com',
                [doctor.email, patient.email],
                fail_silently=False,
            )

        # Perform any actions needed for a completed and accepted appointment
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DoctorDashboardView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        current_month = timezone.now().month
        appointments = Appointment.objects.filter(doctor=user, date__month=current_month)

        total_appointments = appointments.count()
        total_accepted_appointments = appointments.filter(decision='ACCEPTED').count()
        total_rejected_appointments = appointments.filter(decision='REJECTED').count()

        data = {
            'total_appointments': total_appointments,
            'total_accepted_appointments': total_accepted_appointments,
            'total_rejected_appointments': total_rejected_appointments,
        }

        return Response(data)
