from django import forms

from menu.models import MenuItem

from .models import Order


class OrderCreateForm(forms.Form):
    menu_item = forms.ModelChoiceField(queryset=MenuItem.objects.filter(is_available=True))
    quantity = forms.IntegerField(min_value=1, initial=1)


class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ("status",)
