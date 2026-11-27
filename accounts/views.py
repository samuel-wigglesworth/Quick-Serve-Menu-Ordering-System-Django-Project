from django.contrib.auth import login
from django.shortcuts import redirect, render

from customers.models import CustomerProfile

from .forms import SignupForm


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data["email"]
            user.is_staff = form.cleaned_data["is_staff_member"]
            user.save()
            CustomerProfile.objects.get_or_create(user=user)
            login(request, user)
            return redirect("dashboard")
    else:
        form = SignupForm()
    return render(request, "accounts/signup.html", {"form": form})
