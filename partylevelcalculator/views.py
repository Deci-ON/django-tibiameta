# views.py
from django.shortcuts import render
from .forms import MeuFormulario
import math

def partylevelcalculator(request):
    if request.method == 'POST':
        form = MeuFormulario(request.POST)
        try:
            if form.is_valid():
                meu_campo = form.cleaned_data['meu_campo']
                max_level = (meu_campo/2)
                max_level = math.ceil(max_level*3)
                min_level = (meu_campo/3)
                min_level = math.ceil(min_level*2)
                context ={
                    'form': form,
                    'meu_campo': meu_campo,
                    'max_level': max_level,
                    'min_level': min_level
                }

                return render(request, 'tibiameta/partylevelcalculator.html', context)
        except Exception:
            context={
                'error': 'Error on calc, try again'
            }
            
            return render(request, 'tibiameta/partylevelcalculator.html', context)

            
    else:
        form = MeuFormulario()
    return render(request, 'tibiameta/partylevelcalculator.html', {'form': form})
