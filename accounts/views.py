from django.shortcuts import render
from django.http import HttpResponse
from .models import CustomUser
from .serializers import CustomUserSerializer
from django.contrib.auth import authenticate, login, logout

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.authtoken.models import Token
from rest_framework import generics

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from .serializers import CustomTokenObtainPairSerializer


class AllUserView(generics.ListCreateAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [
        # IsAuthenticated
        AllowAny
    ]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return CustomUser.objects.all()
        return CustomUser.objects.filter(id=user.id)

    # def perform_create(self, serializer):
    #     if self.request.user.is_superuser:
    #         serializer.save()
    # else:
    #     raise PermissionDenied("Only admins can create new users.")


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "message": "User created successfully",
                    "user": {
                        "username": user.username,
                        "email": user.email,
                        "phone": user.phone,
                    },
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        # Validate input
        if not email or not password:
            return Response(
                {"message": "Email and password are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(request, email=email, password=password)

        if user is not None:
            # Get or create token - note: get_or_create returns (token, created)
            token, created = Token.objects.get_or_create(user=user)

            return Response(
                {
                    "message": "User logged in successfully",
                    "token": token.key,  # Now we access the token object's key
                    "user": {
                        "username": user.username,
                        "email": user.email,
                        "phone": user.phone,
                    },
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {"message": "Invalid Email or Password"},
            status=status.HTTP_401_UNAUTHORIZED,
        )


class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        logout(request)
        return Response(
            {"message": "User logged out successfully"},
            status=status.HTTP_200_OK,
        )


class UserAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, request):
        return request.user

    def get(self, request):
        user = self.get_object(request)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        user = self.get_object(request)
        serializer = CustomUserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Account updated successfully", "user": serializer.data},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = self.get_object(request)
        user.delete()
        return Response(
            {"message": "Account deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
