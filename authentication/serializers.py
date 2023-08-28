from .models import User
from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField


class UserCreationSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(max_length=30)
    email = serializers.EmailField(max_length=50)
    user_type = serializers.ChoiceField(choices=User.USER_TYPES)
    phone_number = PhoneNumberField(allow_blank=False)
    password = serializers.CharField(min_length=8)

    class Meta:
        model = User
        fields = ['fullname', 'email', 'user_type', 'phone_number', 'password']

    def validate(self, attrs):
        email_exists = User.objects.filter(email=attrs['email']).exists()

        if email_exists:
            raise serializers.ValidationError(
                detail='User with email already exists'
            )

        phone_number_exists = User.objects.filter(phone_number=attrs['phone_number']).exists()

        if phone_number_exists:
            raise serializers.ValidationError(
                detail='User with phone number already exists'
            )

        return super().validate(attrs)

    def create(self, validated_data):
        user = User.objects.create_user(
            fullname=validated_data['fullname'],
            email=validated_data['email'],
            user_type=validated_data['user_type'],
            phone_number=validated_data['phone_number']
        )

        user.set_password(validated_data['password'])
        user.save()
        return user


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']

