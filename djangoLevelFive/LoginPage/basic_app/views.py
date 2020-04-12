from django.shortcuts import render
from basic_app import forms

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from  django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, 'basic_app/index.html')

def register(request):

# Check for registeration
    registered = False

    if request.method == "POST":
        user_form = forms.UserForm(request.POST)
        profile_form = forms.UserProfileInfoForm(request.POST)

        # Validate data
        if user_form.is_valid() and profile_form.is_valid():

            # save user data in User table
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            # Mapping of user in profile model
            profile = profile_form.save(commit=False)
            profile.user = user

            # Check if profile pic is provided
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = forms.UserForm()
        profile_form = forms.UserProfileInfoForm()

    contex_dict={'user_form':user_form,
                'profile_form':profile_form,
                'registered':registered}

    return render(request, 'basic_app/register.html', contex_dict)

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse('<h1>OPP you seems to be inactive from very long time</h1>')
        else:
            return HttpResponse('<H1> Well username:{} and password:{} is wrong'.format(username,password))
    else:
        return render(request, 'basic_app/user_login.html', {})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def special_page(request):
    return HttpResponse('<h1>This page required login ....</h1>')
