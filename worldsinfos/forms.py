from django import forms
from django.utils import timezone
from django.forms.widgets import SelectDateWidget

class WorldForm(forms.Form):
    world = forms.TypedChoiceField(
        choices=(),
        required=True,
        label='',
        widget=forms.Select(attrs={
            'class': 'form-control form-select select2',
            'data-bs-placeholder': 'Select Loyalty'
        })
    )

    def __init__(self, *args, **kwargs):
        choices = kwargs.pop('choices', ())
        super(WorldForm, self).__init__(*args, **kwargs)
        self.fields['world'].choices = choices