from django.db import models
from registrar.models import AllCourses

from django.contrib.auth import get_user_model
User=get_user_model()

class RegisteredCourses(models.Model):
    student =models.ForeignKey(User, on_delete=models.CASCADE)  
    code=models.ForeignKey(AllCourses, on_delete=models.CASCADE)
    select=models.BooleanField(default=False)



