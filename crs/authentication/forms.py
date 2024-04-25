
from django import forms
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import get_user_model
User=get_user_model()

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=254)
    password = forms.CharField(max_length=63, widget=forms.PasswordInput)

class SignupForm(UserCreationForm):  
    class Meta(UserCreationForm.Meta):  
        model=User
        fields=('email', 'first_name', 'last_name')

    # To remove help text for password creation. Overrirde the default behaviour.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        