from django.urls import path

from cssf.views.rp.compras.create import ComprasCreateView
from cssf.views.rp.compras.list import ComprasListView
from cssf.views.rp.empresa.create import EmpresaCreateView
from cssf.views.rp.empresa.list import EmpresaListView
from cssf.views.rp.personas.create import PersonaCreateView
from cssf.views.rp.personas.delete import PersonasDeleteView
from cssf.views.rp.personas.list import PersonaListView
from cssf.views.rp.personas.update import PersonasUpdateView
from cssf.views.rp.views_rp import *

app_name = "rp"

urlpatterns = [
    path('index/', mainIndex, name="index"),
    path('inventario/', listarstocksustancias, name="inventario"),
    path('inventario/movimientos/', listarmovimientoinventario, name="movimientoinventario"),
    path('compras/', ComprasListView.as_view(), name="compras"),
    path('compras/registro/', ComprasCreateView.as_view(), name="registrocompras"),
    path('solicitudes/', listarsolicitudesentregasustancias, name="listadosolicitudes"),
    path('solicitudes/registro/', registrarsolicitidentregasustancias, name="entregasustancias"),
    path('empresas/', EmpresaListView.as_view(), name="empresas"),
    path('empresas/registro/', EmpresaCreateView.as_view(), name="registroempresa"),
    path('personas/', PersonaListView.as_view(), name="personas"),
    path('personas/registro/', PersonaCreateView.as_view(), name="registropersonas"),
    path('personas/update/<int:pk>/', PersonasUpdateView.as_view(), name="actualizacionpersonas"),
    path('personas/delete/<int:pk>/', PersonasDeleteView.as_view(), name="eliminarpersonas"),
]
