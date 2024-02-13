from .models import *
from django import forms

class CustomCityForm(forms.Form):
    city_id = forms.ModelChoiceField(
        queryset=City.objects.all(),
        empty_label="Select OR Search City",
        label="City",
        widget=forms.Select(attrs={'class': 'form-control city_id form-select'}),
        required=True
    )