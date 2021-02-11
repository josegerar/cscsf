from django.shortcuts import render

def bodIndex(request):
    data = {
        "urls": [
            {
                "uridj": "bdg:index",
                "uriname": "Home"
            }
        ],
        "usertitle": "Bodeguero/a",
        "title": "Home"
    }
    return render(request, 'homebdg.html', data)

def ingresarcomprabdg(request):
    data = {
        "urls": [
            {
                "uridj": "bdg:index",
                "uriname": "Home"
            },
            {
                "uridj": "bdg:ingresocompras",
                "uriname": "Ingresar"
            }
        ],
        "usertitle": "Bodegruero/a",
        "title": "Ingresar compras"
    }
    return render(request, "ingresarcompras.html", data)

def entregasustanciabdg(request):
    data = {
        "urls": [
            {
                "uridj": "bdg:index",
                "uriname": "Home"
            },
            {
                "uridj": "bdg:entregasustancias",
                "uriname": "Entregar"
            }
        ],
        "usertitle": "Bodegruero/a",
        "title": "Entregar sustancias"
    }
    return render(request, "entregasustancias.html", data)

def movimientobdg(request):
    data = {
        "urls": [
            {
                "uridj": "bdg:index",
                "uriname": "Home"
            },
            {
                "uridj": "bdg:movimientoinv",
                "uriname": "Movimiento"
            }
        ],
        "usertitle": "Bodegruero/a",
        "title": "Movimiento de Inventario"
    }
    return render(request, "movimientoinv.html", data)

def stockbdg(request):
    data = {
        "urls": [
            {
                "uridj": "bdg:index",
                "uriname": "Home"
            },
            {
                "uridj": "bdg:stockinv",
                "uriname": "Stock"
            }
        ],
        "usertitle": "Bodegruero/a",
        "title": "Stock de Inventario"
    }
    return render(request, "stockinv.html", data)