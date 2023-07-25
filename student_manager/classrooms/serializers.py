from rest_framework import serializers
from commons.exceptions import ValidationException
from .models import ClassRoom
from datetime import datetime
from django.conf import settings

class CreateClassRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassRoom
        fields = "__all__"

class DetailsClassRoomSerializer(serializers.ModelSerializer):
    updated_date = serializers.SerializerMethodField()
    created_date = serializers.SerializerMethodField()
    name = serializers.CharField(max_length=200)

    class Meta:
        model = ClassRoom
        fields = [
            "id",
            "name",
            "created_date",
            "updated_date"
        ]

    def get_updated_date(self, data):
        data = data.updated_date
        return data.strftime(settings.DATE_TIME_FORMAT) if data else None
    
    def get_created_date(self, data):
        data = data.created_date
        return data.strftime(settings.DATE_TIME_FORMAT) if data else None

class DeleteClassRoomSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        instance.deleted_at = datetime.now()
        instance.save()
        return instance

    class Meta:
        model = ClassRoom
        fields = ""
