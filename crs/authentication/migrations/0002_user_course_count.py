# Generated by Django 5.0.4 on 2024-04-25 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='course_count',
            field=models.IntegerField(default=0),
        ),
    ]
