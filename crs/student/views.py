from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import SelectCourseFormSet
#from datetime import datetime
from . import forms
from registrar.models import ListCourses, AllCourses
from .models import RegisteredCourses
from django.db.models import F

from django.contrib.auth import get_user_model
User=get_user_model()

from django.http import HttpResponse

@login_required   
def student_home(request):
    return render(request, 'student/student_home.html')

@login_required  
def student_home(request):
    #curr_datetime = datetime.now() #if curr_datetime #registration_status=False
    
    courses=ListCourses.objects.all()  
    if request.method == 'POST': 
        formset = SelectCourseFormSet(request.POST)  # Binding the POST data to the formset
        if formset.is_valid():    
            selected_courses_count = 0
            for form, course in zip(formset, courses):
                if form.clean()['select'] == True:  # clean() is a custom method based on cleaned_data() defined in SelectCourseForm class
                    selected_courses_count += 1
                    selected_course=ListCourses.objects.get(code = course.code.pk)
                    if selected_course.student_count > 19:
                        failure=True
                        message='<span style="display: inline; color: red;">Error:</span> You cannot select a course which has more than 20 students.'
                        return render(request, 'student/success_failure.html', {'message':message, 'failure':failure})
            
            if 3 <= selected_courses_count <= 6:
                for form, course in zip(formset, courses):
                    status = form.clean()['select']
                    print(status)
                    reg_course= RegisteredCourses.objects.create(
                        student= User.objects.get(email = request.user),  # user_id is FK in model class, so it must be an instance of User class.
                        code = course.code,
                        select = status
                    )

                    if status == True:
                        course.student_count = F('student_count') + 1
                        course.save()
                        #ListCourses.objects.filter(pk = course.code_id).update(student_count = F('student_count') + 1)
                    
                    reg_course.save()
            

                
                # Now student has registered. Change registration_status to True.
                user_object = User.objects.get(email = request.user)
                user_object.registration_status = True
                user_object.save() 
                #print(user_object.registration_status)
                failure=False
                message=f'You have successfully registered for {selected_courses_count} courses'
            
            else:
                failure=True
                message='<span style="display: inline; color: red;">Error:</span> You are only allowed to register for minimum of 3 and maximum of 6 courses.'    
            
            return render(request, 'student/success_failure.html', {'message' : message, 'failure':failure})
        
        else:
            formset = SelectCourseFormSet() 
            return render(request, 'student/student_home.html', {'formset' : formset, 'courses' : courses})
    
    else:  # request method is GET
    
        formset = SelectCourseFormSet() 
        return render(request, 'student/student_home.html', {'courses':courses, 'formset': formset})

    


@login_required
def view_courses(request):
    #return HttpResponse("You have already registered")

    registered_courses = RegisteredCourses.objects.filter(student= User.objects.get(email = request.user), select=True) 
    print(registered_courses)
    #registered_courses=[]
    #for objects in registered_courses_query_set:
    #    registered_courses.append(objects.code.code_id)

    context = {'registered_courses' : registered_courses}
    
    return render(request, 'student/view_courses.html', context )

    
    