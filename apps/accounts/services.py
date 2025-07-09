import random
from apps.accounts.models import *
from tools.exceptions import CustomAPIException
import logging 
from tools.redis import redis_client
from authentication.jwt import CustomRefreshToken
from rest_framework_simplejwt.exceptions import AuthenticationFailed


logger = logging.getLogger('django')

class CustomUserService:
    def __init__(self):
        pass

    def verify_otp(self, email, otp: int):
        existing_otp = redis_client.get(f"user:{email}")
        if existing_otp == str(otp):
            return True
        return False

    def send_verification_code(self, email):
        user = CustomUser.objects.filter(email=email).first()

        if not user:        
            otp = random.randint(1000, 9999)
            redis_client.set(f"user:{email}", otp, 300)
            print("DEBUG OTP", otp)
            return True

        raise CustomAPIException(detail="User already exist", error_code="UserAlreadyExist")
    
    
    def create_user(self, email=None, password=None, **validated_data):
        try:
            user = CustomUser.objects.create(email=email)
            user.set_password(password)
            user.save()
            
        except Exception as e:
            raise CustomAPIException(detail=str(e), error_code="UserAlreadyExist")
        
        return self.update_user(email=email, **validated_data)

       
    def update_user(self, email:str, **update_fields):
        user = CustomUser.objects.get(email=email)
        for field , value in update_fields.items():
            if value != "":
                setattr(user, field, value)
        
        user.save()
        return user
    
    def login_user(self, email, password):
        user = CustomUser.objects.filter(email=email).first()

        if not user:
            raise CustomAPIException(detail="User not found", error_code="UserNotFound")
        print("password", password)
        if not user.check_password(password):
            raise CustomAPIException(detail="Invalid Password", error_code="InvalidPassword")
        
        if not user.is_active:
            raise AuthenticationFailed("User is not active")
        
        refresh = CustomRefreshToken.for_user(user)

        return str(refresh), str(refresh.access_token)


 