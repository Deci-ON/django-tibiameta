from django.shortcuts import render
from django.http import HttpResponse
from django.db import connections
from django.http import JsonResponse
from datetime import datetime


def top100exp(request):
    try:
        with connections['tibia_meta'].cursor() as cursor:
            cursor.execute("SET @rank=0;")
            cursor.execute(f"SELECT @rank:=@rank+1 AS rank, char_name, format(char_exp,0), format(char_exp_change,0), char_level, char_vocation, char_world, coalesce (SEC_TO_TIME(char_time*60),'00:00:00') as online_time ,char_voc_rank, char_world_rank FROM tibia_stats.char_experience_calc WHERE char_info_ref = (select max(char_info_ref) from tibia_stats.char_experience_calc) order by char_exp_change desc limit 100;")
            rows= cursor.fetchall()
            context={
                'data':rows
            }
        return render(request,'tibiameta/top100exp.html', context)
    except Exception as e:
        print(e)
        return render(request,'tibiameta/404.html')

def search(request):
    if request.method == 'POST':
        selected_date = request.POST.get('calendario')
        try:
            data = datetime.strptime(selected_date, "%Y-%m-%d")
            date = data.strftime("%d/%m/%Y")
            with connections['tibia_meta'].cursor() as cursor:
                        cursor.execute("SET @rank=0;")
                        cursor.execute(
                    "SELECT @rank:=@rank+1 AS rank, char_name, format(char_exp,0), format(char_exp_change,0), char_level, char_vocation, char_world, coalesce (SEC_TO_TIME(char_time*60),'00:00:00') as online_time ,char_voc_rank, char_world_rank FROM tibia_stats.char_experience_calc WHERE char_info_ref = %s order by char_exp_change desc limit 100;",
                    [selected_date]
                )                   
                        rows= cursor.fetchall()
                        context={
                    'data':rows,
                    'date': date
                }
            return render(request, 'tibiameta/top100exp.html', context)
        except Exception as e:
            context={
                'date_error': 'Please select a valid date'
            }
            return render(request,'tibiameta/top100exp.html', context)

    return render(request, 'template.html')


