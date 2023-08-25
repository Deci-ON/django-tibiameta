
# meuapp/forms.py
from django import forms

class Expcalculatorforms(forms.Form):
    field1 = forms.IntegerField(label='Initial Level', required=False)
    field2 = forms.IntegerField(label='Desired Level')
    opcional = forms.IntegerField(label='Opcional, your experience to calc.' , required=False)
