# forms.py
from django import forms

class playersForm(forms.Form):
    player1 = forms.CharField(
        min_length=3,
        max_length=40,
        label="Character",
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'placeholder': 'Character',
            'required': "True",
        })
    )


import requests
from django.http import JsonResponse

class ServerSearchForm(forms.Form):
    server_name = forms.ChoiceField(
        label='Server Name',
        choices=[],
        widget=forms.Select(attrs={'class': 'form-control form-select', 'style':'text-align: center; ', 'placeholder': 'Search by servers'}),
    )
    
    def __init__(self, *args, **kwargs):
        super(ServerSearchForm, self).__init__(*args, **kwargs)
        self.fields['server_name'].choices = self.get_server_names()
        
    level_field = forms.IntegerField(
        label="Level",
        min_value=1,  # Defina o valor mínimo
        max_value=5000,  # Defina o valor máximo
        widget=forms.NumberInput(attrs={
            'class': "form-control",
            'placeholder': 'Level',
            'required': "True",
        })
    )

    def clean_level_field(self):
        level_field = self.cleaned_data['level_field']
        if not str(level_field).isdigit():
            raise forms.ValidationError('Please enter a valid integer.')
        return level_field

    def get_server_names(self):
        try:
            api_url = "https://api.tibiadata.com/v4/worlds"
            response = requests.get(api_url)
            if response.ok:
                data = response.json()
                server_names = [
                    ('Search by server', 'Search by server'),  # Novo item adicionado
                ] + [
                    (server_data['name'], server_data['name'])
                    for server_data in data.get('worlds', {}).get('regular_worlds', [])
                ]

                return server_names

        except requests.exceptions.HTTPError as errh:
            print("HTTP Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print("OOps: Something went wrong", err)
        return JsonResponse({'success': False, 'error_message': 'Please, try again.'})


