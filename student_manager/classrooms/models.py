from django.db import models

class ClassRoom(models.Model):
    name = models.CharField(max_length=200, unique=True, null=True)
    deleted_at = models.DateTimeField(max_length=(6), null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True, max_length=(6))
    created_date = models.DateTimeField(auto_now_add=True, max_length=(6))
    
    class Meta:
        db_table = "classroom"
