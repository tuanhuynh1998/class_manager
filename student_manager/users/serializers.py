from rest_framework import serializers
from .models import User
from django.conf import settings
from datetime import datetime
from dj_rest_auth.registration.serializers import RegisterSerializer

class UserRegisterSerializer(RegisterSerializer):
    username = serializers.CharField(max_length=150)
    first_name = serializers.CharField(required=False, default="")
    last_name = serializers.CharField(required=False, default="")
    email = serializers.CharField(
        required=False, default="", allow_blank=True, allow_null=True
    )

class CreateUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "is_superuser",
            "password"
        ]
        extra_kwargs = {'password': {'write_only': True, 'min_length': 4}}

    def create(self, validated_data):
        check_superuser = validated_data.pop('is_superuser', None)
        if check_superuser:
            data = User.objects.create_superuser(**validated_data)
        else:
            data = User.objects.create_user(**validated_data)
        return data

class DetailsUserSerializer(serializers.ModelSerializer):
    updated_date = serializers.SerializerMethodField()
    created_date = serializers.SerializerMethodField()
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(max_length=254)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "created_date",
            "updated_date"
        ]

    def get_updated_date(self, data):
        data = data.updated_date
        return data.strftime(settings.DATE_TIME_FORMAT) if data else None
    
    def get_created_date(self, data):
        data = data.created_date
        return data.strftime(settings.DATE_TIME_FORMAT) if data else None

    def update(self, instance, validated_data):
        instance.username = validated_data['username']
        instance.save()
        return instance
        
class DeleteUserSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        instance.deleted_at = datetime.now()
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ""
