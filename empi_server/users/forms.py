from .models import EmpiUser

from django import forms
from django.core.exceptions import ValidationError


class RegistrationForm(forms.Form):
    email = forms.EmailField()
    full_name = forms.CharField()
    role = forms.ChoiceField(widget=forms.RadioSelect, choices={
        "SU": "Supervízor",
        "EX": "Expert",
        "PA": "Študent"
    })
