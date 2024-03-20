from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
import logging
from rest_framework import status
from tools.exceptions import CustomAPIException
from apps.accounts.services import CustomUserManagerV2
from authentication.firebase import FirebaseAuthentication
from firebase_admin.exceptions import *
from apps.accounts.models import CustomUser

logger = logging.getLogger('django')


class RegisterAPI(APIView):
    class InputSerializer(serializers.ModelSerializer):
        uid = serializers.UUIDField(default=None)
        email = serializers.EmailField(default=None)
        password = serializers.CharField(required=False)
        device_id = serializers.CharField(required=False)

        class Meta:
            model = CustomUser
            fields = "__all__"
        
    def _get_firebase_user(self, request):
        fra = FirebaseAuthentication()
        return fra.get_firebase_user(request=request)
    

    def post(self, request, *args,  **kwargs):
        firebase_user = self._get_firebase_user(request=request)
        print(firebase_user.uid)
        serializer = self.InputSerializer(data=request.data) 
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            raise CustomAPIException(detail=str(e), error_code="MissingFieldError")
        
        user_manager = CustomUserManagerV2(uid=firebase_user.uid)
        if not firebase_user.provider_data:
            user = user_manager.create_guest_user(**request.data)
            return Response({"data": UserSerializer(user).data})

        user = user_manager.create_user(**request.data)
        return Response({"data": UserSerializer(user).data})
        
        
    def patch(self, request, *args,  **kwargs):
        firebase_user = self._get_firebase_user(request=request)
        user_manager = CustomUserManagerV2(uid=firebase_user.uid)
        user = user_manager.update_user(**request.data)
        return Response({"data": UserSerializer(user).data})

class DeviceEligibleForGuest(APIView):
    class InputSerializer(serializers.Serializer):
        device_id = serializers.CharField()

    def get(self, request):
        serializer = self.InputSerializer(data=request.GET)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            raise CustomAPIException(detail=str(e), error_code="MissingFieldError")
        
        manager = CustomUserManagerV2()
        device_eligible = manager.device_eligible_for_guest_user(**serializer.data)
        if not device_eligible:
            raise CustomAPIException(error_code="GuestUserLoginLimitExceed")
        
        return Response({"data": {"msg":"Device Eligible."}})


class PhoneNumberExistanceAPI(APIView):
    def get(self, request):
        try:
            phone_number = request.GET["phone_number"]
            firebase_user = self._get_user_by_phone(phone_number=phone_number)
            
            try:
                self._update_phone_number(firebase_user=firebase_user, phone_number=phone_number)
            except Exception as e:
                print("Error in phone number updation.")
                return Response({"is_exist": False}, status=status.HTTP_200_OK)

            return Response({"is_exist": True}, status=status.HTTP_200_OK)
        
        except KeyError as e:
            # need for missingFieldError
            return Response({"code":"missing_key", "msg": str(e) }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        except Exception as e:
            return Response({"is_exist": False, "msg": f"phone_number not found {e}" }, status=status.HTTP_200_OK)
        
    def _get_user_by_phone(self, phone_number):
        firebase_user = FirebaseAuthentication.get_user_by_phone_number(self, phone_number=phone_number)
        return firebase_user
    
    def _update_phone_number(self, firebase_user, phone_number):
        user = CustomUser.objects.get(uid=firebase_user.uid)
        if user.phone_number != phone_number:
            user.phone_number = phone_number
            user.save()
    