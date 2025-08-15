
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Gender


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password1', 'password2'
        ]


class UserProfileForm(forms.ModelForm):
    birth_date = forms.CharField(
        widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(
        choices=Gender.choices, widget=forms.Select(attrs={'class': 'dropdown'}))

    class Meta:
        model = Profile
        fields = [
            'first_name', 'last_name', 'birth_date', 'gender', 'image'
        ]
