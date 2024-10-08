from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import loginform
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


@login_required()
def home_view(request):
    return render(request, "homehtml.html")


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
                return render(request, "registration/login.html", {"form2": form1})
    else:
        form1 = loginform()

    return render(request, "registration/login.html", {"form2": form1})


def logout_view(request):
    logout(request)
    return redirect("loginurl")


def signup_view(request):
    try:

        if request.method == "POST":
            signupform = UserCreationForm(request.POST)
            if signupform.is_valid():
                signupform.save()
                return redirect("loginurl")
            else:
                return render(request, "signuphtml.html", {"signformtohtml": signupform, "msg": "invalid login"})

        else:
            signupform = UserCreationForm()
            return render(request, "signuphtml.html", {"signformtohtml": signupform, "msg": "invalid submission"})
    except Exception as e:
        print(e)
        signupform = UserCreationForm()
        return render(request, "signuphtml.html", {"signformtohtml": signupform})


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
