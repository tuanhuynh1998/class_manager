from rest_framework import serializers
from .models import Subject
from django.conf import settings
from datetime import datetime

class CreateSubjectSerializer(serializers.ModelSerializer):
    updated_date = serializers.SerializerMethodField()
    created_date = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = [
            "name",
            "updated_date",
            "created_date"
        ]

    def get_updated_date(self, data):
        data = data.updated_date
        return data.strftime(settings.DATE_TIME_FORMAT) if data else None
    
    def get_created_date(self, data):
        data = data.created_date
        return data.strftime(settings.DATE_TIME_FORMAT) if data else None

class DetailsSubjectSerializer(serializers.ModelSerializer):
    updated_date = serializers.SerializerMethodField()
    created_date = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = [
            "name",
            "updated_date",
            "created_date"
        ]

    def get_updated_date(self, data):
        data = data.updated_date
        return data.strftime(settings.DATE_TIME_FORMAT) if data else None
    
    def get_created_date(self, data):
        data = data.created_date
        return data.strftime(settings.DATE_TIME_FORMAT) if data else None

class DeleteSubjectSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        instance.deleted_at = datetime.now()
        instance.save()
        return instance

    class Meta:
        model = Subject
        fields = ""
