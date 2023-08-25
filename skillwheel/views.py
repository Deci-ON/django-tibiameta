from django.shortcuts import render

# Create your views here.
  
  
def skill_wheel(request):
  return render(request, 'tibiameta/skillwheel.html')  
    