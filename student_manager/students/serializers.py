from rest_framework import serializers
from .models import Student
from django.conf import settings
from datetime import datetime

class CreateStudentSerializer(serializers.ModelSerializer):
    updated_date = serializers.SerializerMethodField()
    created_date = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = "__all__"

    def get_updated_date(self, data):
        data = data.updated_date
        return data.strftime(settings.DATE_TIME_FORMAT) if data else None
    
    def get_created_date(self, data):
        data = data.created_date
        return data.strftime(settings.DATE_TIME_FORMAT) if data else None

class DetailsStudentSerializer(serializers.ModelSerializer):
    updated_date = serializers.SerializerMethodField()
    created_date = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = "__all__"

    def get_updated_date(self, data):
        data = data.updated_date
        return data.strftime(settings.DATE_TIME_FORMAT) if data else None
    
    def get_created_date(self, data):
        data = data.created_date
        return data.strftime(settings.DATE_TIME_FORMAT) if data else None

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

class DeleteStudentSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        instance.deleted_at = datetime.now()
        instance.save()
        return instance

    class Meta:
        model = Student
        fields = ""
