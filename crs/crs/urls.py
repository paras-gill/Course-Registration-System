"""
URL configuration for crs project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

import authentication.views
import registrar.views  
import professor.views
import student.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', authentication.views.login_page, name='login'),
    path('logout/', authentication.views.logout_user, name='logout'),
    path('signup/', authentication.views.signup_page, name='signup'),

    path('registrarHome/', registrar.views.registrar_home, name='registrarHome'),
    path('registrarHome/createCourse', registrar.views.create_course, name='createCourse'),
    path('registrarHome/uploadCourse', registrar.views.upload_course, name='uploadCourse'),
    path('registrarHome/profSignUp', registrar.views.prof_signup_page, name='profSignUp'),
    path('registrarHome/resetSemester', registrar.views.reset_semester, name='resetSemester'),
    
    path('studentHome1/', student.views.student_home, name='studentHome1'),
    path('studentHome2/', student.views.view_courses, name='studentHome2'),
    
    path('professorHome/', professor.views.professor_home, name='professorHome'),

]
