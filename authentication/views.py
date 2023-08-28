from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework.response import Response

from authentication import serializers


# Create your views here.
class UserCreateView(generics.GenericAPIView):
    serializer_class = serializers.UserCreationSerializer

    def post(self, request):
        data = request.data

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        return Response(data=serializer.data, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(generics.GenericAPIView):
    serializer_class = serializers.UserLoginSerializer

    def post(self, request):
        data = request.data

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user = authenticate(email=email, password=password)

            if user:
                return Response(status=status.HTTP_200_OK)

            return Response(data={'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)