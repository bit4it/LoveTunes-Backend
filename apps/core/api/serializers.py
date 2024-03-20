from rest_framework import serializers
from apps.core.models  import CustomErrors


class ErrorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomErrors
        fields = "__all__"