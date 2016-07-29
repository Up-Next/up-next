from django import forms
from .models import Party


class PartyForm(forms.ModelForm):
    required_css_class = "required"
    error_css_class = "error"
    class Meta:
        model = Party
        fields = ('party_name', 'url', 'user_nickname',)
