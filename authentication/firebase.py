import os
import firebase_admin
from django.conf import settings
from apps.accounts.models import CustomUser
from django.utils import timezone
from firebase_admin import auth
from firebase_admin import credentials
from rest_framework import authentication
from rest_framework import exceptions
from .exceptions import ExpiredAuthToken, FirebaseError, UserAlreadyRegistered
from .exceptions import InvalidAuthToken
from .exceptions import NoAuthToken
from decouple import config

cred = credentials.Certificate({
        "type": "service_account",
        "project_id": config('FIREBASE_PROJECT_ID'),
        "private_key_id": config('FIREBASE_PRIVATE_KEY_ID'),
        "private_key": config('FIREBASE_PRIVATE_KEY').replace('\\n', '\n'),
        "client_email": config('FIREBASE_CLIENT_EMAIL'),
        "client_id": config('FIREBASE_CLIENT_ID'),
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": config('FIREBASE_CLIENT_CERT_URL')
    })

default_app = firebase_admin.initialize_app(cred)


class FirebaseAuthentication(authentication.BaseAuthentication):
    
    def authenticate(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION")
  
        # if not auth_header:
        #     raise NoAuthToken("No auth token provided")

        # id_token = auth_header.split(" ").pop()
        # decoded_token = None

        # try:
        #     decoded_token = auth.verify_id_token(id_token)            
        # except Exception:
        #     raise InvalidAuthToken("Invalid/expired auth token")

        # if not id_token or not decoded_token:
        #     return None

        try:
            uid = "3cd0DdgLpNQZmoOnsbLgWbrcYh13"
            # uid = decoded_token.get("uid")
        except Exception:
            raise FirebaseError()
        
        try:
            user = CustomUser.objects.get(uid=uid)
            user.last_login = timezone.localtime()
        except Exception:
            raise InvalidAuthToken("Please register this token first @ /api/v1/accounts/user/register/")
        return (user, uid)
    
    def get_firebase_user(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION") 
        # testing purpose
        if request.GET.get("is_testing", False):
            return auth.get_user(uid="3cd0DdgLpNQZmoOnsbLgWbrcYh13") 

        if not auth_header:
            raise NoAuthToken("No auth token provided")
        
        id_token = auth_header.split(" ").pop()
        decoded_token = None

        try:
            decoded_token = auth.verify_id_token(id_token)            
        except Exception:
            raise InvalidAuthToken("Invalid/expired auth token")

        try:
            uid = decoded_token.get("uid")
            # uid = "V9OAhabvv9QQSTD2t98UIvehqS92" # testing purpose
        except Exception:
            raise FirebaseError()
       
        return auth.get_user(uid=uid) 
    
    def get_uid_from_token(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        uid = auth_header.split(" ").pop()
        decoded_token = auth.verify_id_token(uid)
        uid = decoded_token.get('uid')
        return uid  
     
    def get_user_from_token(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        uid = auth_header.split(" ").pop()
        decoded_token = auth.verify_id_token(uid)
        uid = decoded_token.get('uid')
        try:
            user = CustomUser.objects.get(uid=uid)
        except:
            raise InvalidAuthToken("Please register this token first @ /api/v1/accounts/user/register/")

        return user 
      
    def get_user_from_auth_token(self, auth_token):
        uid = auth_token.split(" ").pop()
        decoded_token = auth.verify_id_token(uid)
        uid = decoded_token.get('uid')
        print(uid)
        # uid = "3O7tSphxWRVUpwIjgC8hhWZnPXD3"
        try:
            user = CustomUser.objects.get(uid=uid)
        except:
            raise InvalidAuthToken("Please register this token first @ /api/v1/accounts/user/register/")

        return user   
