from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser
from apps.accounts.managers import CustomUserManager
import uuid
from django.core.exceptions import ValidationError
from django.utils import timezone

# Create your models here.
class CustomUser(AbstractUser):
    uuid = models.CharField(max_length=255, unique=True, default=uuid.uuid1)
    uid = models.CharField(max_length=255, unique=True, primary_key=True) # add unique=True
    username = models.CharField(verbose_name="username",max_length=122, unique=True, null=True,blank=True)
    email = models.EmailField(verbose_name='email', unique=True)
    is_email_verified = models.BooleanField(default=False)
    firebase_token = models.CharField(max_length=255, null=True, blank=True) # add unique=True
    first_name  = models.CharField(max_length=20, null=True, blank=True)
    last_name  = models.CharField(max_length=20, null=True, blank=True)
    phone_number  = models.CharField(max_length=20, null=True, blank=True)
    STATUS_OPTION = (
        ("1", "Online"),
        ("2", "Offline")
    )
    status = models.CharField(max_length=122,choices=STATUS_OPTION, default="2")
    address_line_1 = models.CharField(max_length=200, null=True, blank=True)
    address_line_2 = models.CharField(max_length=200, null=True, blank=True)
    zip_code = models.CharField(max_length=6, null=True, blank=True)
    country = models.CharField(max_length=20, null=True, blank=True)
    country_code = models.IntegerField(default=91) # 91 for india.
    date_of_birth = models.DateField(null=True, blank=True)
    # is_premium = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    updated_on = models.DateTimeField(auto_now=True)
    # admin_of_groups = models.ManyToManyField("chatbot.chatroom", null=True, blank=True, related_name="admins")
    is_guest = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.uid
   
    def change_status(self, status):
        self.status = status
        self.save()
        return self.status
    
    def guest_user_services(self):
        services = self.guest_service.services.all()
        return services


class Device(models.Model):
    users = models.ManyToManyField(CustomUser, related_name="devices")
    device_id = models.CharField(max_length=255, unique=True)
    is_logged_in = models.BooleanField(default=False)
    fcm_token = models.CharField(max_length=255, null=True, blank=True) # add unique=True
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.device_id)
    
    def logout(self):
        self.is_logged_in = False
        self.save()

    def login(self):
        self.is_logged_in = True
        self.save()

    def update_fcm_token(self, fcm_token):
        self.fcm_token = fcm_token
        self.save()

    def update_user(self, user):
        self.user = user
        self.save()

