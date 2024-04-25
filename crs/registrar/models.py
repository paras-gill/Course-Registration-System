from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

from django.contrib.auth import get_user_model
User=get_user_model()


class AllCourses(models.Model):
    code=models.CharField(max_length=10, unique=True)  
    name=models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class ListCourses(models.Model):
    
    code = models.ForeignKey(AllCourses, on_delete = models.CASCADE)
    professor = models.ForeignKey(User, on_delete = models.CASCADE, limit_choices_to = {'role' : 'Professor'})
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    
    max_students = models.IntegerField(validators = [
        MinValueValidator(1),  
        MaxValueValidator(100), 
        ])
    
    student_count = models.IntegerField(default=0)

    def __str__(self):
        return self.code.name

