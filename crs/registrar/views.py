from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from . import forms
from .models import ListCourses, AllCourses
from student.models import RegisteredCourses
from django.db.models import F

from django.contrib.auth import get_user_model
User=get_user_model()


@login_required  
def registrar_home(request):
    return render(request, 'registrar/registrar_home.html')


@login_required
def create_course(request):
    if request.method == 'POST':
        form = forms.CreateCourseForm(request.POST)
        if form.is_valid():
            course_code=form.cleaned_data['code']
            course_name=form.cleaned_data['name']
            message=f'<span><strong>{course_code} - {course_name}</strong></span> course has been created. This course can now be listed for registration.'
            form.save()
            return render(request, 'registrar/success_failure.html', {'message' : message})
    else:
        form = forms.CreateCourseForm() 
    return render(request, 'registrar/create_course.html', {'form': form})



@login_required
def upload_course(request):
    if request.method == 'POST':
        form = forms.ListCoursesForm(request.POST)
        if form.is_valid(): 
            
            # Increment course_count for prof after he has been assigned course
            professor=form.cleaned_data['professor']
            professor_object = User.objects.get(email=professor)
            User.objects.filter(pk=professor_object.pk).update(course_count = F('course_count') + 1)

            course_name=form.cleaned_data['code']
            course_code=AllCourses.objects.get(name=course_name).code
            message=f'<strong>{course_code} - {course_name}</strong> course has been successfully listed for registration.'

            form.save()
            return render(request, 'registrar/success_failure.html', {'message' : message} )  
    else:
        if len(AllCourses.objects.all())==len(ListCourses.objects.all()):
            message='<span style="color:red;">No course left to be listed!<span>'
            return render(request, 'registrar/success_failure.html', {'message' : message} )
        form = forms.ListCoursesForm()
    return render(request, 'registrar/upload_course.html', {'form': form})


@login_required
def prof_signup_page(request):   
    form = forms.ProfSignUpForm()   
    message=''  
    if request.method == 'POST': 
        form = forms.ProfSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()  
            message = f'Professor {user.first_name} {user.last_name} Signed up successfully.'
        else:
            message="Signup faled because invalid signup details provided. Signup Again!"
        return render(request, 'registrar/success_failure.html', context={'message':message})
    else:
        form = forms.ProfSignUpForm()
        return render(request, 'registrar/prof_signup.html', context={'form':form, 'message':message})



@login_required
def reset_semester(request):  
    
    """
    1. Delete all objects from ListCourses model
    2. Delete all objects from RegisteredCourses model
    3. Update 'registration_status' and 'course_count' field of User model
    
    """

    if request.method == 'GET':
        RegisteredCourses.objects.all().delete()
        ListCourses.objects.all().delete()  # Comment this if you do not want to un list all the listed courses.
        User.objects.all().update(course_count=0)
        User.objects.filter(role='Student').update(registration_status=False)
        message='No course listed now. Go back to homePage to list courses again'
        return render(request, 'registrar/success_failure.html', context={'message':message})



@login_required
def all_students(request):
    students=User.objects.filter(role='Student')
    return render(request, 'registrar/all_students.html', {'students': students})



@login_required
def all_professors(request):
    professors=User.objects.filter(role='Professor')
    return render(request, 'registrar/all_professors.html', {'professors': professors})