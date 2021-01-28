from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

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
    return render(request, 'rp/homerp.html', data)


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
    return render(request, "rp/registrocompras.html", data)


def listarcompras(request):
    data = {
        "urls": [
            {
                "uridj": "rp:index",
                "uriname": "Home"
            },
            {
                "uridj": "rp:compras",
                "uriname": "Compras"
            }
        ],
        "usertitle": "Representante Técnico",
        "title": "Compras registradas",
        "icontitle": "store-alt",
        "laboratorios": Laboratorio.objects.all()
    }
    return render(request, "rp/listarcompras.html", data)


class ListarComprasView(ListView):
    model = ComprasPublicas
    template_name = "rp/listarcompras.html"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            data = Laboratorio.objects.get(pk=request.POST['id']).toJSON()
        except Exception as e:
            data["error"] = str(e)
        return JsonResponse(data)

    def get_queryset(self):
        return ComprasPublicas.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usertitle'] = "Representante Técnico"
        context['title'] = "Compras registradas"
        context['icontitle'] = "store-alt"
        context['laboratorios'] = Laboratorio.objects.all()
        context['urls'] = [
            {
                "uridj": "rp:index",
                "uriname": "Home"
            },
            {
                "uridj": "rp:compras",
                "uriname": "Compras"
            }
        ]
        return context


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
