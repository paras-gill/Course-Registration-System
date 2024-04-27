from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from registrar.models import ListCourses, AllCourses

from django.contrib.auth import get_user_model
User=get_user_model()

@login_required  
def professor_home(request):
    courses_teaching=ListCourses.objects.filter(professor=User.objects.get(email = request.user))
    #course_code = professor_field.pk
    #course_name = AllCourses.objects.get(code = course_code).name
    #context={'course_code' : course_code, 'course_name' : course_name}
    
    return render(request, 'professor/professor_home.html', {'courses_teaching' : courses_teaching})