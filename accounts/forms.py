from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    is_staff_member = forms.BooleanField(
        required=False,
        help_text="Enable for restaurant staff accounts.",
        label="Register as staff",
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2", "is_staff_member")
