from django.shortcuts import render

def bodIndex(request):
    return render(request, 'bdg/homebdg.html')