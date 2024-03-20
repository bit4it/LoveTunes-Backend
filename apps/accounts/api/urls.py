from django.contrib import admin
from django.urls import path, include
from apps.accounts.api import views


urlpatterns = [
    path("user/register/", views.RegisterAPI.as_view(), name="register"),
    # path("user/phone-number/exist/", views..as_view(), name="phone_numberexist")
]

