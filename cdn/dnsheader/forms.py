from django import forms

class DnsForm(forms.Form):
    domain = forms.URLField(label='Domain', max_length=200)
    cdn = forms.CharField(label='CDN', max_length=200)
