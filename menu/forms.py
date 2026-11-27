from django import forms

from .models import MenuItem


class MenuItemForm(forms.ModelForm):
    image_url = forms.CharField(
        required=False,
        widget=forms.URLInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com/image.jpg',
            }
        ),
        help_text="Paste a public image URL for the menu item photo",
    )

    class Meta:
        model = MenuItem
        fields = ("name", "description", "price", "is_available", "image_url")
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
