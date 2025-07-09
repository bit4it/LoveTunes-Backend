from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser
from apps.accounts.managers import CustomUserManager
import uuid
from django.core.exceptions import ValidationError
from django.utils import timezone

# Create your models here.import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    uid = models.CharField(max_length=255, unique=True, primary_key=True, auto_created=True, default=uuid.uuid4)
    username = models.CharField(verbose_name="username", max_length=122, unique=True, null=True, blank=True)
    email = models.EmailField(verbose_name='email', unique=True)
    is_email_verified = models.BooleanField(default=False)
    firebase_token = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    
    STATUS_CHOICES = (
        ("online", "Online"),
        ("offline", "Offline"),
        ("listening", "Listening")  # Added for music context
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="offline")
    
    is_premium = models.BooleanField(default=False)  # Important for music app
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email or self.uid
   
    def change_status(self, status):
        self.status = status
        self.save()
        return self.status