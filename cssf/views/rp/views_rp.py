from django.shortcuts import render

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
        "icontitle": "store-alt"
    }
    return render(request, "rp/listarcompras.html", data)

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