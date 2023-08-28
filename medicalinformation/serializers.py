from rest_framework import serializers

from authentication.models import User
from .models import MedicalInformation


class MedicalInformationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    gender = serializers.ChoiceField(choices=MedicalInformation.GENDER_CHOICES)
    blood_group = serializers.ChoiceField(choices=MedicalInformation.BLOOD_GROUPS)
    age = serializers.IntegerField(max_value=100)
    medical_history = serializers.CharField(max_length=500)
    allergies = serializers.CharField(max_length=300)
    medications = serializers.CharField(max_length=300)

    class Meta:
        model = MedicalInformation
        fields = ['user', 'gender', 'blood_group', 'age', 'medical_history', 'allergies', 'medications']
