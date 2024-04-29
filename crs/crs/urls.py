from django.urls import path

import authentication.views
import registrar.views  
import professor.views
import student.views

urlpatterns = [
    path('', authentication.views.login_page, name='login'),
    path('logout/', authentication.views.logout_user, name='logout'),
    path('signup/', authentication.views.signup_page, name='signup'),

    path('registrarHome/', registrar.views.registrar_home, name='registrarHome'),
    path('registrarHome/createCourse', registrar.views.create_course, name='createCourse'),
    path('registrarHome/uploadCourse', registrar.views.upload_course, name='uploadCourse'),
    path('registrarHome/profSignUp', registrar.views.prof_signup_page, name='profSignUp'),
    path('registrarHome/resetSemester', registrar.views.reset_semester, name='resetSemester'),
    path('registrarHome/allStudents', registrar.views.all_students, name='allStudents'),
    path('registrarHome/allProfessors', registrar.views.all_professors, name='allProfessors'),
    
    path('studentHome1/', student.views.student_home, name='studentHome1'),  # If registration_status = False
    path('studentHome2/', student.views.view_courses, name='studentHome2'),  # If registration_status = True
    
    path('professorHome/', professor.views.professor_home, name='professorHome'),

]
