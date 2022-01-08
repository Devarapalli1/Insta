from django import forms
from django.db import models
from django.forms import fields
from instagramapp.models import Post, Users
from django.core.exceptions import ValidationError
from django.core import validators


def UniqueUser(value):
    if Users.objects.filter(user_name__iexact=value).exists():
        raise ValidationError("User name should be unique.")


def UniqueEmail(value):
    if Users.objects.filter(email__iexact=value).exists():
        raise ValidationError("User exists with this maid id")


"""
    username = forms.CharField(widget=forms.TextInput(), max_length=30, required=True,)
	email = forms.CharField(widget=forms.EmailInput(), max_length=100, required=True,)
	password = forms.CharField(widget=forms.PasswordInput())
	confirm_password = forms.CharField(widget=forms.PasswordInput(), required=True, label="Confirm your password.")

	class Meta:

		model = User
		fields = ('username', 'email', 'password')

	def __init__(self, *args, **kwargs):
		super(SignupForm, self).__init__(*args, **kwargs)
		self.fields['username'].validators.append(ForbiddenUsers)
		self.fields['username'].validators.append(InvalidUser)
		self.fields['username'].validators.append(UniqueUser)
		self.fields['email'].validators.append(UniqueEmail)
"""


class UserForm(forms.ModelForm):
    user_name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "User Name"}),
        max_length=30,
        required=True,
        validators=[UniqueUser],
        label="",
    )
    email = forms.CharField(
        widget=forms.EmailInput(attrs={"placeholder": "Email Address"}),
        max_length=100,
        required=True,
        validators=[UniqueEmail],
        label="",
    )

    class Meta:
        model = Users
        exclude = ["date_created"]
        widgets = {
            "email": forms.EmailInput(attrs={"placeholder": "Email Address"}),
            "name": forms.TextInput(attrs={"placeholder": "Full Name"}),
            "user_name": forms.TextInput(attrs={"placeholder": "User Name"}),
            "password": forms.PasswordInput(attrs={"placeholder": "Password"}),
        }
        labels = {
            "email": "",
            "name": "",
            "user_name": "",
            "password": "",
        }


class LoginForm(forms.Form):
    user_name = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "Enter User Name"}),
    )
    password = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={"placeholder": "Password"},
        ),
    )


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["description", "location", "post"]
        widgets = {"description": forms.Textarea(attrs={"cols": 50})}
        labels = {
            "description": "Description",
            "location": "Location",
            "post": "",
        }
