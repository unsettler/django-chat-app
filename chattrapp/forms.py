from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUsercreated


class loginform(forms.Form):
    username1 = forms.CharField(
        max_length=100,
        label="Username",  # Adjusting label
        widget=forms.TextInput(attrs={'class': 'form-inputs', 'placeholder': 'Enter your username'})
    )
    password1 = forms.CharField(
        label="Password",  # Adjusting label
        widget=forms.PasswordInput(attrs={'class': 'form-inputs', 'placeholder': 'Enter your password'})
    )


class Profilepictureform(forms.ModelForm):
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = CustomUsercreated
        fields = ['profile_picture']


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=False, help_text="Enter a valid email address.")

    class Meta:
        model = CustomUsercreated
        fields = ('username', 'password1', 'password2', "email")


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUsercreated
        fields = ['username', 'email']
