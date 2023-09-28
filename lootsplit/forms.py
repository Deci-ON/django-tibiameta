from django import forms

class TextInputForm(forms.Form):
    text_input = forms.CharField(widget=forms.Textarea(attrs={
            'textarea class': "form-control mb-4",
            'placeholder': "Input your party hunt",
            "rows": "4",
            }))
    