from django.urls import path

from core.representantetecnico.views.compras.create import ComprasCreateView
from core.representantetecnico.views.compras.list import ComprasListView
from core.representantetecnico.views.empresa.create import EmpresaCreateView
from core.representantetecnico.views.empresa.list import EmpresaListView
from core.representantetecnico.views.personas.create import PersonaCreateView
from core.representantetecnico.views.personas.delete import PersonasDeleteView
from core.representantetecnico.views.personas.list import PersonaListView
from core.representantetecnico.views.personas.update import PersonasUpdateView
from core.representantetecnico.views.repositorio.list import RepositorioListView
from core.representantetecnico.views.views_rp import mainIndex, listarstocksustancias, listarmovimientoinventario, \
    listarsolicitudesentregasustancias, registrarsolicitidentregasustancias

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

    path('repositorio/', RepositorioListView.as_view(), name="repositorio"),
    path('repositorio/<int:pk>/', RepositorioListView.as_view(), name="repositorioid"),
]
