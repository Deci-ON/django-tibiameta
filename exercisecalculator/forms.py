# myapp/forms.py

from django import forms
from .models import Vocations, Skills 


class Calcform(forms.Form):
    current_skill = forms.IntegerField(
        required=True,
        min_value=10,
        widget=forms.NumberInput(attrs={
            'class': "form-control mb-4 is-invalid state-invalid",
            'placeholder': 'Current Skill',
            'required': "True",
            'type': 'number',
        })
    )
    percent_skill = forms.FloatField(
        required=True,
        widget=forms.NumberInput(attrs={
            'class': "form-control mb-4 is-invalid state-invalid",
            'placeholder': 'Percent Skill',
            'required': "True",
            'type': 'number',
            'oninput': 'percent(this.value)',
        })
    )
    desired_skill = forms.IntegerField(
        required=True,
        min_value=10,
        widget=forms.NumberInput(attrs={
            'class': "form-control mb-4 is-invalid state-invalid",
            'placeholder': 'Desired Skill',
            'required': "True",
            'type': 'number',
        })
    )
    loyalty = forms.ChoiceField(
        choices=(("0", 'Disabled'),
        ("1", "360 - 5%"),
        ("2", "720 - 10%"),
        ("3", "1080 - 15%"),
        ("4", "1440 - 20%"),
        ("5", "1800 - 25%"),
        ("6", "2160 - 30%"),
        ("7", "2520 - 35%"),
        ("8", "2880 - 40%"),
        ("9", "3240 - 45%"),
        ("10", "3600 - 50%")),
        widget=forms.Select(attrs={
            'class': 'form-control form-select select2',
            'data-bs-placeholder': 'Select Loyalty'
        })
    )
    double_event = forms.BooleanField(required=False, widget=forms.CheckboxInput)
    private_dummy = forms.BooleanField(required=False, widget=forms.CheckboxInput)
    
    vocation = forms.ModelChoiceField(queryset=Vocations.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control',"hx-get": "load_skills/", "hx-target": "#id_skills"}))
    skills = forms.ModelChoiceField(queryset=Skills.objects.none(), widget=forms.Select(attrs={'class': 'form-control'}) )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "vocation" in self.data:
            vocations_id = int(self.data.get("vocation"))
            self.fields["skills"].queryset = Skills.objects.filter(vocations_id=vocations_id)