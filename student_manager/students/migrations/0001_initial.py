# Generated by Django 3.2.8 on 2022-05-30 06:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('classrooms', '__first__'),
        ('subjects', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('age', models.PositiveIntegerField(blank=True, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('tel', models.CharField(blank=True, max_length=20, null=True, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, max_length=6, null=True)),
                ('updated_date', models.DateTimeField(auto_now=True, max_length=6)),
                ('created_date', models.DateTimeField(auto_now_add=True, max_length=6)),
                ('classroom', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='classrooms.classroom')),
                ('subjects', models.ManyToManyField(to='subjects.Subject')),
            ],
            options={
                'db_table': 'student',
            },
        ),
    ]