
from django import forms
from .models import AllCourses, ListCourses
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Subquery

from django.contrib.auth import get_user_model
User=get_user_model()


class CreateCourseForm((forms.ModelForm)):
    class Meta:
        model = AllCourses
        fields = ['code', 'name']


class ListCoursesForm(forms.ModelForm):  
    class Meta:  
        model = ListCourses
        fields = ['code', 'professor', 'start_date', 'end_date', 'max_students']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
    
    def __init__(self, *args, **kwargs): 
        super(ListCoursesForm, self).__init__(*args, **kwargs) 
        
        # Exclude coursess already selected in the form

        
        listed_courses_pks=ListCourses.objects.values_list('code_id', flat=True) 
        # flat = True specifies that the result should be a flat list rather than a list of tuples.
        
        courses_available=AllCourses.objects.exclude(pk__in=Subquery(listed_courses_pks)) 
        course_choices=[(course.id, f'{course.code} - {course.name}') for course in courses_available]
        self.fields['code'].choices = course_choices
        self.fields['code'].label = 'Course'
        
        professors=User.objects.filter(role='Professor')
        professor_choices=[(prof.id, f'Prof. {prof.first_name} {prof.last_name} ({prof.course_count})') for prof in professors] # Prof. <f_name> <l_nam> (no. of courses)
        self.fields['professor'].choices = professor_choices

        
class ProfSignUpForm(UserCreationForm):    
    class Meta(UserCreationForm.Meta): 
        model=User   
        fields=('email', 'first_name', 'last_name')
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'Professor'  # Set the role field to 'Professor' before saving to db
        if commit:
            user.save()
        return user
    
    # To remove help text for password creation. Overrirde the default behaviour.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
    
    