from django import forms
from .models import RegisteredCourses
from registrar.models import ListCourses

class SelectCourseForm(forms.ModelForm):  
    select = forms.BooleanField(widget=forms.CheckboxInput(attrs={'label': False}), required=False)

    class Meta:
        model = RegisteredCourses
        fields = ['select'] 
    
    def clean(self,):
        cleaned_data = super().clean()
        
        # If the checkbox is not in the cleaned_data, set it to False
        if 'select' not in cleaned_data:
            cleaned_data['select'] = False
        return cleaned_data

    # To hide label of this form field in the table
    #def __init__(self, *args, **kwargs):
    #    super().__init__(*args, **kwargs)
    #    self.fields['select'].label = False

total_listed_courses = len(ListCourses.objects.all()) 
#print(total_listed_courses)   
SelectCourseFormSet = forms.formset_factory(SelectCourseForm, extra=total_listed_courses)

'''
Why do we use forms.ModelForm as subclass instead of forms.Form ?

In Django, when you're working with forms that are closely tied to models, it's often convenient to use forms.ModelForm 
instead of forms.Form. Here's why:

1. Automatic Form Fields: When you use forms.ModelForm, Django automatically generates form fields based on the fields of 
the corresponding model. This saves you from having to manually define each form field. It ensures that your form fields 
correspond directly to the fields in your model, making it easy to create, update, and validate forms.

2. Validation: With forms.ModelForm, Django automatically performs validation based on the model field definitions. This 
includes validating field types, max lengths, unique constraints, and any other constraints defined in the model. It helps 
ensure data integrity and reduces the amount of validation code you need to write manually.

3. Saving Data: When you call form.save() on a form created with forms.ModelForm, Django automatically creates or updates 
model instances based on the form data. It handles the process of saving data to the database, including handling relationships 
between models.

4. Integration with Templates: When rendering forms in templates, forms.ModelForm provides helper methods like {{ form.as_p }}, 
{{ form.as_table }}, and {{ form.as_ul }}, which automatically generate HTML markup for rendering the form fields in paragraph, 
table, or unordered list format. This makes it easy to render forms in templates without writing much HTML.

While forms.ModelForm is convenient for working with model-related forms, there are cases where forms.Form may be more appropriate. 
For example, if you need a form that's not directly tied to a model or if you need more control over the form fields, you can use 
forms.Form and define the fields manually.
'''