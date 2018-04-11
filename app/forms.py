"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _


class TextForm(forms.Form):
    text_search = forms.CharField(label='Text Search', max_length=100)

class SelectYear(forms.Form):
           year = forms.CharField(widget=forms.Select)


