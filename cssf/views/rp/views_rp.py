from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from cssf.forms.rp.formCompra import ComprasForm
from cssf.models import *


def mainIndex(request):
    data = {
        "urls": [
            {
                "uridj": "rp:index",
                "uriname": "Home"
            }
        ],
        "usertitle": "Representante Técnico",
        "title": "Home"
    }
    return render(request, 'rp/home.html', data)


def listarmovimientoinventario(request):
    data = {
        "urls": [
            {
                "uridj": "rp:index",
                "uriname": "Home"
            },
            {
                "uridj": "rp:inventario",
                "uriname": "Inventario"
            },
            {
                "uridj": "rp:movimientoinventario",
                "uriname": "Movimientos"
            }
        ],
        "usertitle": "Representante Técnico",
        "title": "Movimientos inventario"
    }
    return render(request, "rp/listarmovimientosinventario.html", data)


def listarstocksustancias(request):
    data = {
        "urls": [
            {
                "uridj": "rp:index",
                "uriname": "Home"
            },
            {
                "uridj": "rp:inventario",
                "uriname": "Inventario"
            }
        ],
        "usertitle": "Representante Técnico",
        "title": "Inventario"
    }
    return render(request, "rp/listarstocksustancias.html", data)


def registrarcompra(request):
    data = {
        "urls": [
            {
                "uridj": "rp:index",
                "uriname": "Home"
            },
            {
                "uridj": "rp:compras",
                "uriname": "Compras"
            },
            {
                "uridj": "rp:registrocompras",
                "uriname": "Registro"
            }
        ],
        "usertitle": "Representante Técnico",
        "title": "Registrar compra"
    }
    return render(request, "rp/compras/create.html", data)




def registrarsolicitidentregasustancias(request):
    data = {
        "urls": [
            {
                "uridj": "rp:index",
                "uriname": "Home"
            },
            {
                "uridj": "rp:listadosolicitudes",
                "uriname": "Solicitudes"
            },
            {
                "uridj": "rp:entregasustancias",
                "uriname": "Registro"
            }
        ],
        "usertitle": "Representante Técnico",
        "title": "Registro entrega sustancias"
    }
    return render(request, "rp/solicitudentregasustancias.html", data)


def listarsolicitudesentregasustancias(request):
    data = {
        "urls": [
            {
                "uridj": "rp:index",
                "uriname": "Home"
            },
            {
                "uridj": "rp:listadosolicitudes",
                "uriname": "Solicitudes"
            }
        ],
        "usertitle": "Representante Técnico",
        "title": "Solicitudes resgistradas"
    }
    return render(request, "rp/listarsolicitudesentregasustancias.html", data)
