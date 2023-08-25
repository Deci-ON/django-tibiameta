# forms.py
from django import forms

class MeuFormulario(forms.Form):
    meu_campo = forms.IntegerField(label='')

    def clean_meu_campo(self):
        meu_campo = self.cleaned_data['meu_campo']
        if meu_campo and not str(meu_campo).isnumeric():
            raise forms.ValidationError('Please, only valid numbers')
        return meu_campo