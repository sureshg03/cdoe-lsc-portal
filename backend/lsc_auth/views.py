from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json
from .models import LSCUser
from django.core.exceptions import ValidationError
import re
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class LSCLoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['lsc_number'] = user.lsc_number
        token['lsc_name'] = user.lsc_name
        return token

class LSCLoginView(TokenObtainPairView):
    serializer_class = LSCLoginSerializer
    permission_classes = [AllowAny]

class LSCLogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'message': 'Logout successful'})

class ChangePasswordView(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

        old_password = request.data.get('oldPassword')
        new_password = request.data.get('newPassword')

        if not old_password or not new_password:
            return Response({'error': 'Old and new passwords are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate password strength
        if len(new_password) < 8 or not re.search(r'[A-Z]', new_password) or not re.search(r'[0-9]', new_password):
            return Response({'error': 'New password must be at least 8 characters long and include uppercase letters and numbers'}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Password changed successfully'})
        else:
            return Response({'error': 'Incorrect old password'}, status=status.HTTP_400_BAD_REQUEST)