# --encoding: utf-8

from django import forms


class PublicationsCreate(forms.Form):
    name = forms.CharField(max_length=150)


