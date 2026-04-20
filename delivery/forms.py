from django import forms

from .models import DeliveryStatus


class DeliveryStatusForm(forms.ModelForm):
    class Meta:
        model = DeliveryStatus
        fields = ("rider_name", "current_location", "eta")
