from django import forms

class LogForm(forms.Form):
    file = forms.FileField()