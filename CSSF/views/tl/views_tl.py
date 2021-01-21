from django.shortcuts import render

def labIndex(request):
    return render(request, 'tl/hometl.html')