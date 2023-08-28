from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.response import Response
from . import serializers
from .models import MedicalInformation, User
from rest_framework.permissions import IsAuthenticated

User = get_user_model()


# Create your views here.
class CreateListMedicalInformation(generics.GenericAPIView):
    serializer_class = serializers.MedicalInformationSerializer
    queryset = MedicalInformation.objects.all()
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_summary="get medical record for a user")
    def get(self, request):
        medical_information = MedicalInformation.objects.all()
        serializer = self.serializer_class(instance=medical_information, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_summary="Create medical record for a user")
    def post(self, request):
        data = request.data

        serializer = self.serializer_class(data=data)

        user = request.user

        if serializer.is_valid():
            serializer.save(patient=user)

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FilterUsersByMedicalRecordView(generics.ListAPIView):
    serializer_class = serializers.MedicalInformationSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_summary="Get medical record based on medical condition")
    def get_queryset(self):
        medical_condition = self.request.query_params.get('medical_condition')
        if medical_condition:
            users_with_condition = MedicalInformation.objects.filter(medical_history__icontains=medical_condition)
            return users_with_condition.values_list('user', flat=True)
        return MedicalInformation.objects.none()


class GetAllMedicalRecords(generics.ListAPIView):
    serializer_class = serializers.MedicalInformationSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_summary="Get all medical records")
    def get_queryset(self):
        if self.request.user.user_type != 'HEALTH_WORKER':
            return MedicalInformation.objects.none()

        return MedicalInformation.objects.all()
