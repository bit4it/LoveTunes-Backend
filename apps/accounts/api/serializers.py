from rest_framework import serializers
from apps.accounts.models import CustomUser


class UserSerializer(serializers.Serializer):
    uid = serializers.UUIDField(read_only=True)
    email = serializers.EmailField(read_only=True)
    phone_number = serializers.CharField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    full_name = serializers.SerializerMethodField(read_only=True)
    is_premium = serializers.BooleanField(read_only=True)
    status = serializers.CharField(read_only=True)
    created_on = serializers.DateTimeField(read_only=True)
    updated_on = serializers.DateTimeField(read_only=True)


    def get_full_name(self, obj):
        return f"{obj.first_name or ''} {obj.last_name or ''}".strip()
