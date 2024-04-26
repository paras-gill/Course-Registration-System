from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout  
from . import forms


def logout_user(request):
    logout(request)   
    return redirect ('login')


def login_page(request):
    form = forms.LoginForm()
    message = request.session.get('message', '')
    
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)  
                if user.role=='Registrar':
                    return redirect('registrarHome')
                #elif user.role=='Professor':
                #    return redirect('professorHome')
                elif user.role=='Student':
                    #print(user.registration_status)
                    if user.registration_status==True:
                        #print('redirecting home 2')
                        return redirect('studentHome2')
                    else:
                        #print('redirecting home 1')
                        return redirect('studentHome1')
            else:
                message = 'Login failed! Incorrect email or password'
    return render(request, 'authentication/login.html', context={'form': form, 'message': message})



def signup_page(request):   
    form = forms.SignupForm()    
    if request.method == 'POST':  
        if not form:
            return render(request, 'authentication/signup.html', context={'form': form})
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            form.save()  
            request.session['message']='Sign Up Successful. Login Here!'
            return redirect('login') 
    return render(request, 'authentication/signup.html', context={'form': form})  
    