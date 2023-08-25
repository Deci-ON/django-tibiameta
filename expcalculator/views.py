from django.shortcuts import render

# meuapp/views.py
from django.shortcuts import render
from .forms import Expcalculatorforms


def experiencia_necessaria_v2(level):
    return (50 / 3) * (level**3 - 6 * level**2 + 17 * level - 12)

def expcalculator(request):
    if request.method == 'POST':
        form = Expcalculatorforms(request.POST)
        show_messages = False
        if form.is_valid():
            try:
                # Faça algo com os dados válidos aqui
                level = form.cleaned_data['field1']
                desired_level = form.cleaned_data['field2']
                exp_atual = form.cleaned_data['opcional']
                if exp_atual is not None:
                    desired_exp = int(experiencia_necessaria_v2(desired_level))
                    calc = int(desired_exp - exp_atual)
                    form = Expcalculatorforms()
                    show_messages = True
                    context={
                        'ini_exp':exp_atual,
                        'desired_level': desired_level,
                        'des_exp': desired_exp,
                        'calc': calc,
                        'form': form,
                        'show_messages': show_messages
                    }
                    return render(request, 'tibiameta/expcalculator.html', context)                         
                else:
                    desired_exp = int(experiencia_necessaria_v2(desired_level))
                    ini_exp = int(experiencia_necessaria_v2(level))
                    calc = int(desired_exp - ini_exp)
                    form = Expcalculatorforms()
                    show_messages = True
                    context = {
                        'level': level,
                        'desired_level': desired_level,
                        'ini_exp':ini_exp,
                        'des_exp': desired_exp,
                        'calc': calc,
                        'form': form,
                        'show_messages': show_messages
                    }
                    return render(request, 'tibiameta/expcalculator.html', context) 
                
                form = Expcalculatorforms()
            except Exception:
                return render(request, 'tibiameta/expcalculator.html', {'form': form})

    else:
        form = Expcalculatorforms()

    return render(request, 'tibiameta/expcalculator.html', {'form': form})
