from django import forms
from django.contrib.auth.forms import UserCreationForm
# from .models import CustomUsercreated


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


# class CustomUserCreationForm(UserCreationForm):
#     profile_picture = forms.ImageField(required=False)
#
#     class Meta:
#         model = CustomUsercreated
#         fields = ('username', 'password1', 'password2', 'profile_picture')
