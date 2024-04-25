from django.db import models

from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    PROFESSOR = 'Professor'
    STUDENT = 'Student'
    REGISTRAR='Registrar'
  
    ROLE_CHOICES = (
        (PROFESSOR, 'Professor'),
        (STUDENT, 'Student'),
        (REGISTRAR, 'Registrar'),
    )
     
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='Student') 

    email = models.EmailField(unique=True) 
    username=None
    USERNAME_FIELD = 'email'
   
    registration_status=models.BooleanField(default=False) 
    REQUIRED_FIELDS = []
    
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    course_count=models.IntegerField(default=0)

    objects = CustomUserManager()   