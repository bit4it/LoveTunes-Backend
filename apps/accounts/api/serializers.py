from rest_framework import serializers
from apps.accounts.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = CustomUser

class BasicUserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["uid", "email", "phone_number", "first_name","last_name"]
        model = CustomUser