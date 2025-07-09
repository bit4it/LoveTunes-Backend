from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
import logging
from tools.exceptions import CustomAPIException
from apps.accounts.services import CustomUserService
from apps.accounts.models import CustomUser
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

logger = logging.getLogger('django')


class RegisterAPI(APIView):
    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField(required=True, max_length=255)
        first_name = serializers.CharField(max_length=50, default="")
        last_name = serializers.CharField(max_length=50, default="")
        password = serializers.CharField(required=True)
        otp = serializers.CharField(required=True)


    def post(self, request, *args,  **kwargs):
        serializer = self.InputSerializer(data=request.data) 
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            raise CustomAPIException(detail=str(e), error_code="MissingFieldError")
        
        user_manager = CustomUserService()

        if not user_manager.verify_otp(email=serializer.data["email"], 
                                       otp=serializer.data["otp"]):
            raise CustomAPIException(detail="Invalid OTP", error_code="InvalidOTP")

        user = user_manager.create_user(**serializer.data)
        return Response({"data": UserSerializer(user).data})
    


class LoginAPI(APIView):
    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField(required=True, max_length=255)
        password = serializers.CharField(required=True)

    def post(self, request, *args,  **kwargs):
        serializer = self.InputSerializer(data=request.data) 
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            raise CustomAPIException(detail=str(e), error_code="MissingFieldError")
        
        user_manager = CustomUserService()

        refresh_token, access_token = user_manager.login_user(**serializer.data)

        return Response({"access_token": access_token, "refresh_token": refresh_token})
        
class SendVerificationOTPAPI(APIView):
    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField(required=True, max_length=255)


    def get(self, request, *args,  **kwargs):
        serializer = self.InputSerializer(data=request.GET.copy()) 
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            raise CustomAPIException(detail=str(e), error_code="MissingFieldError")
        
        user_manager = CustomUserService()

        user_manager.send_verification_code(serializer.data["email"])

        return Response({"message": "OTP sent successfully! OTP will expire in 5 minutes"})
        
class UpdateUserAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    class InputSerializer(serializers.Serializer):
        first_name = serializers.CharField(max_length=50, default="")
        last_name = serializers.CharField(max_length=50, default="")

    
    def patch(self, request, *args,  **kwargs):
        serializer = self.InputSerializer(data=request.data) 
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            raise CustomAPIException(detail=str(e), error_code="MissingFieldError")
        
        user_manager = CustomUserService()
        user = user_manager.update_user(email=request.user.email, **serializer.data)
        return Response({"data": UserSerializer(user).data})