from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .forms import loginform
from django.contrib.auth.forms import UserCreationForm
from .forms import Profilepictureform
from .forms import CustomUserCreationForm
from .models import CustomUsercreated, Message
from .models import Message
from django.db.models import Q

User = get_user_model()


@login_required()
def home_view(request):
    return render(request, "homehtml.html",
                  {'current_user': request.user.username, "profile_picture": request.user.profile_picture})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("homeurl")
    form1 = loginform()
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
    form = Profilepictureform(instance=request.user)
    if request.method == 'POST':
        form = Profilepictureform(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            # user = request.user  # Get the currently logged-in user
            # user.profile_picture = form.cleaned_data['profile_picture']
            # user.save()  # Save the user instance with the new image
            form.save()
            return render(request, 'homehtml.html',
                          {'form': form, 'msg': "upload succesfull", 'current_user': request.user.username,
                           "profile_picture": request.user.profile_picture})
        else:
            # form = Profilepictureform(instance=request.user)
            return render(request, 'homehtml.html',
                          {'form': form, "msg": "invalid details", 'current_user': request.user.username})
    return render(request, 'homehtml.html', {'form': form, "msg": "post failed", 'current_user': request.user.username})


def search_view(request):
    if request.method == "POST":

        searchedusername = request.POST.get('searchname')
        userreturned = User.objects.filter(username=searchedusername)
        show_search_result = True
        if userreturned.exists():
            return render(request, 'homehtml.html',
                          {"username3": userreturned.first().username, 'current_user': request.user.username,
                           "profile_picture": request.user.profile_picture,
                           "profile_picture1": userreturned.first().profile_picture,
                           'show_search_result': show_search_result,
                           "userid": userreturned.first().id})
        else:
            return render(request, 'homehtml.html', {"msg": "No records found", 'current_user': request.user.username,
                                                     "profile_picture": request.user.profile_picture})
    else:
        return render(request, 'homehtml.html', {"msg": "post method failed", 'current_user': request.user.username,
                                                 "profile_picture": request.user.profile_picture})


def display_view(request):
    users = CustomUsercreated.objects.all()
    return render(request, "homehtml.html", {'users': users, 'current_user': request.user.username,
                                             "profile_picture": request.user.profile_picture})


def delete_view(request):
    if request.method == "POST":
        uname = request.POST["usernametodelete"]
        pword = request.POST["passwordofuser"]

        try:
            # First, authenticate the user by their username and password
            user = authenticate(username=uname, password=pword)

            if user is not None:
                # If the user is authenticated, delete the user
                user.delete()
                return redirect("loginurl")
            else:
                # If authentication fails, provide a message
                return render(request, "deleteuser.html", {"msg": "Incorrect username or password."})
        except Exception as e:
            print(e)
            return render(request, "deleteuser.html", {"msg": "An error occurred while trying to delete the user."})

    return render(request, "deleteuser.html")


def chat_view(request, recipient_id):
    recipient = User.objects.get(id=recipient_id)
    messages = Message.objects.filter(
        (Q(sender=request.user.id) & Q(receiver=recipient)) |
        (Q(sender=recipient) & Q(receiver=request.user.id))
    ).order_by('timestamp')

    return render(request, 'chatroom.html',
                  {'recipient': recipient,
                   'messages': messages,
                   'room_name': f"{min(request.user.id,recipient_id)}_{max(request.user.id,recipient_id)}",
                   "recipient_id": recipient_id,
                   "userid": request.user.id})
