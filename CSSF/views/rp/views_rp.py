from django.shortcuts import render

def mainIndex(request):
    return render(request, 'rp/homerp.html')