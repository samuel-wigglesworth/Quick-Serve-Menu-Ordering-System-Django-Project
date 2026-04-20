from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .forms import CustomerProfileForm
from .models import CustomerProfile


@login_required
def profile_view(request):
    profile, _ = CustomerProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = CustomerProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
    else:
        form = CustomerProfileForm(instance=profile)

    return render(request, "customers/profile.html", {"form": form})
