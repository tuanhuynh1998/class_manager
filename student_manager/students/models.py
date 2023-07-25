from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=200)
    age = models.PositiveIntegerField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    tel = models.CharField(max_length=20, unique=True, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    classroom = models.ForeignKey(
        "classrooms.ClassRoom", related_name="+", on_delete=models.SET_NULL, null=True, blank=True
    )    
    deleted_at = models.DateTimeField(max_length=(6), null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True, max_length=(6))
    created_date = models.DateTimeField(auto_now_add=True, max_length=(6))
    subjects = models.ManyToManyField('subjects.Subject')

    
    class Meta:
        db_table = "student"


