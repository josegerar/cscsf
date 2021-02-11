from django.shortcuts import render

def labIndex(request):
    data = {
        "urls": [
            {
                "uridj": "bdg:index",
                "uriname": "Home"
            }
        ],
        "usertitle": "Técnico Laboratorista",
        "title": "Home"
    }
    return render(request, 'hometl.html', data)

def entregasustanciatl(request):
    data = {
        "urls": [
            {
                "uridj": "tl:index",
                "uriname": "Home"
            },
            {
                "uridj": "tl:entregasustancias",
                "uriname": "Entregar"
            }
        ],
        "usertitle": "Técnico Laboratorista",
        "title": "Entregar sustancias"
    }
    return render(request, "entregasustanciastl.html", data)

def informestl(request):
    data = {
        "urls": [
            {
                "uridj": "tl:index",
                "uriname": "Home"
            },
            {
                "uridj": "tl:informes",
                "uriname": "Informes"
            }
        ],
        "usertitle": "Técnico Laboratorista",
        "title": "Informes"
    }
    return render(request, "informestl.html", data)

def movimientotl(request):
    data = {
        "urls": [
            {
                "uridj": "tl:index",
                "uriname": "Home"
            },
            {
                "uridj": "tl:movimientoinv",
                "uriname": "Movimiento"
            }
        ],
        "usertitle": "Técnico Laboratorista",
        "title": "Movimiento de Inventario"
    }
    return render(request, "movimientoinvtl.html", data)

def stocktl(request):
    data = {
        "urls": [
            {
                "uridj": "tl:index",
                "uriname": "Home"
            },
            {
                "uridj": "tl:stockinv",
                "uriname": "Stock"
            }
        ],
        "usertitle": "Técnico Laboratorista",
        "title": "Stock de Inventario"
    }
    return render(request, "stockinvtl.html", data)