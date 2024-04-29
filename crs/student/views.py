from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from . import forms
from django.forms import formset_factory
from registrar.models import ListCourses
from .models import RegisteredCourses
from django.db.models import F
#from datetime import datetime

from django.contrib.auth import get_user_model
User=get_user_model()


@login_required  
def student_home(request):
    #curr_datetime = datetime.now() #if curr_datetime #registration_status=False
    total_listed_courses = len(ListCourses.objects.all()) 
    SelectCourseFormSet = formset_factory(forms.SelectCourseForm, extra=total_listed_courses)

    courses=ListCourses.objects.all()  
    if request.method == 'POST': 
        formset = SelectCourseFormSet(request.POST)  
        if formset.is_valid():    
            selected_courses_count = 0
            for form, course in zip(formset, courses):
                if form.clean()['select'] == True:  # clean() is a custom method based on cleaned_data() defined in SelectCourseForm class
                    selected_courses_count += 1
                    selected_course=ListCourses.objects.get(code = course.code.pk)
                    if selected_course.student_count >= selected_course.max_students:
                        failure=True
                        message=f'<strong><span style="display: inline; color: red;">Error:</span></strong> You cannot register for <strong>{selected_course.code.code} - {selected_course.code.name}</strong> course as maximum of <strong>{selected_course.max_students}</strong> students could only register for it.'
                        return render(request, 'student/success_failure.html', {'message' : message, 'failure' : failure})
            
            if 3 <= selected_courses_count <= 6:
                for form, course in zip(formset, courses):
                    status = form.clean()['select']
                    reg_course= RegisteredCourses.objects.create(
                        student= User.objects.get(email = request.user),  # user_id is FK in model class, so it must be an instance of User class.
                        code = course.code,
                        select = status
                    )

                    if status == True:
                        course.student_count = F('student_count') + 1
                        course.save()
                    
                    reg_course.save()
                
                # Now student has registered. Change registration_status to True.
                user_object = User.objects.get(email = request.user)
                user_object.registration_status = True
                user_object.save() 

                failure=False
                message=f'You have successfully registered for {selected_courses_count} courses'
            
            else:
                failure=True
                message='<strong><span style="display: inline; color: red;">Error:</span></strong> You are only allowed to register for minimum of 3 and maximum of 6 courses.'    
            
            return render(request, 'student/success_failure.html', {'message' : message, 'failure':failure})
        
        else:
            formset = SelectCourseFormSet() 
            return render(request, 'student/student_home.html', {'formset' : formset, 'courses' : courses})
    
    else:  
        formset = SelectCourseFormSet() 
        return render(request, 'student/student_home.html', {'courses':courses, 'formset': formset})

    
@login_required
def view_courses(request):
    registered_courses = RegisteredCourses.objects.filter(student= User.objects.get(email = request.user), select=True) 
    context = {'registered_courses' : registered_courses}
    return render(request, 'student/view_courses.html', context )

    
    