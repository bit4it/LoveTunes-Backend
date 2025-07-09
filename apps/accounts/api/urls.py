from django.contrib import admin
from django.urls import path, include
from apps.accounts.api import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path("user/send-otp", views.SendVerificationOTPAPI.as_view(), name="send-otp"),
    path("user/register", views.RegisterAPI.as_view(), name="register"),
    path("user/login", views.LoginAPI.as_view(), name="login"),
    path("user/update", views.UpdateUserAPI.as_view(), name="update"),
    path('user/refresh', TokenRefreshView.as_view(), name='token_refresh')
]

