from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import loginform
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# from .forms import Profilepictureform
from .forms import CustomUserCreationForm
from .models import CustomUsercreated
from django.contrib.auth import get_user_model

User = get_user_model()


@login_required()
def home_view(request):
    return render(request, "homehtml.html", {'current_user': request.user.username})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("homeurl")

    if request.method == "POST":
        form1 = loginform(request.POST)

        if form1.is_valid():
            nme = form1.cleaned_data["username1"]
            pwd = form1.cleaned_data["password1"]
            user = authenticate(request, username=nme, password=pwd)
            if user is not None:
                login(request, user)
                return redirect("homeurl")
            else:

                return render(request, "registration/login.html", {"form2": form1, "msg": "invalid login"})
    else:
        form1 = loginform()

    return render(request, "registration/login.html", {"form2": form1})


def logout_view(request):
    logout(request)
    return redirect("loginurl")


def signup_view(request):
    try:

        if request.method == "POST":
            signupform = CustomUserCreationForm(request.POST)
            if signupform.is_valid():
                signupform.save()
                return redirect("loginurl")
            else:
                return render(request, "signuphtml.html", {"signformtohtml": signupform, "msg": "invalid details"})

        else:
            signupform = CustomUserCreationForm()
            return render(request, "signuphtml.html", {"signformtohtml": signupform, "msg": "post method failed"})
    except Exception as e:
        print(e)
        signupform = CustomUserCreationForm()
    return render(request, "signuphtml.html", {"signformtohtml": signupform, "msg": "raised an error"})


def toreset_view(request):
    return render(request, "resethtml.html")


def resetPassword_view(request):
    uname = request.POST["uname"]
    newpassword = request.POST["pword"]

    try:
        user = User.objects.get(username=uname)
        if user is not None:
            user.set_password(newpassword)
            user.save()
            return render(request, "resethtml.html", {"msg": "password reset sucessfully"})
        else:
            return render(request, "resethtml.html", {"msg": "please provide correct username"})
    except Exception as e:
        print(e)
        return render(request, "resethtml.html", {"msg": "password reset failed"})


def profileupload_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            # user = request.user  # Get the currently logged-in user
            # user.profile_picture = form.cleaned_data['profile_picture']
            # user.save()  # Save the user instance with the new image
            form.save()
            return render(request, 'homehtml.html', {'msg': "upload succesfull"})
        else:
            form = CustomUserCreationForm(instance=request.user)
            return render(request, 'homehtml.html', {'form': form, "msg": "invalid details"})
    form = CustomUserCreationForm(instance=request.user)
    return render(request, 'homehtml.html', {'form': form, "msg": "post failed"})


def search_view(request):
    if request.method == "POST":

        searchedusername = request.POST.get('searchname')
        userreturned = User.objects.filter(username=searchedusername)
        if userreturned.exists():
            return render(request, 'homehtml.html', {"username ": userreturned.first().username})
        else:
            return display(request)
    else:
        return render(request, 'homehtml.html', {"msg": "No records found"})


def display(request):
    users = CustomUsercreated.objects.all()
    return render(request, "homehtml.html", {'users': users})
