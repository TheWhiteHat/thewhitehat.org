from django.db import models
from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=126)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
