from django import forms

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
