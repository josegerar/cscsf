from django.urls import path

from cssf.views.rp.compras.create import ComprasCreateView
from cssf.views.rp.compras.list import ComprasListView
from cssf.views.rp.views_rp import *

app_name = "rp"

urlpatterns = [
    path('index/', mainIndex, name="index"),
    path('inventario/', listarstocksustancias, name="inventario"),
    path('inventario/movimientos/', listarmovimientoinventario, name="movimientoinventario"),
    path('compras/', ComprasListView.as_view(), name="compras"),
    path('compras/registro/', ComprasCreateView.as_view(), name="registrocompras"),
    path('solicitudes/', listarsolicitudesentregasustancias, name="listadosolicitudes"),
    path('solicitudes/registro/', registrarsolicitidentregasustancias, name="entregasustancias")
]
