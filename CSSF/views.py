# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from CSSF.models import Categoria, Facultad

def mainIndex(request):
    return render(request, 'rp/homerp.html')

def bodIndex(request):
    return render(request, 'bdg/indexbdg.html')

def labIndex(request):
    return render(request, 'tl/indexLab.html')

def myfirstview(request):
    data = {
        'name': 'Jose',
        'categoria': Categoria.objects.all()
    }
    return render(request, 'prueba/indexprueba.html', data)

def mysecondview(request):
    data = {
        'name': 'Jose',
        'facultad': Facultad.objects.all()
    }
    return render(request, 'prueba/prueba.html', data)