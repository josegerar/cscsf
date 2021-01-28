from django.urls import path

from cssf.views.rp.views_rp import *

app_name = "rp"

urlpatterns = [
    path('index/', mainIndex, name="index"),
    path('inventario/', listarstocksustancias, name="inventario"),
    path('inventario/movimientos/', listarmovimientoinventario, name="movimientoinventario"),
    path('compras/', ListarComprasView.as_view(), name="compras"),
    path('compras/registro/', registrarcompra, name="registrocompras"),
    path('solicitudes/', listarsolicitudesentregasustancias, name="listadosolicitudes"),
    path('solicitudes/registro/', registrarsolicitidentregasustancias, name="entregasustancias")
]
