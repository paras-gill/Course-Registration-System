# Generated by Django 5.0.4 on 2024-04-25 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registrar', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allcourses',
            name='code',
            field=models.CharField(max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='allcourses',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
