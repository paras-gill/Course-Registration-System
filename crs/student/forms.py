from django import forms
from .models import RegisteredCourses

class SelectCourseForm(forms.ModelForm):  
    select = forms.BooleanField(widget=forms.CheckboxInput(attrs={'label': False}), required=False)

    class Meta:
        model = RegisteredCourses
        fields = ['select'] 
    
    # Override default behaviour of clean() method to return False if check box not selected
    def clean(self,):
        cleaned_data = super().clean()
        if 'select' not in cleaned_data:
            cleaned_data['select'] = False
        return cleaned_data

