from django.urls import path

from core.representantetecnico.views.compras.create import ComprasCreateView
from core.representantetecnico.views.compras.list import ComprasListView
from core.representantetecnico.views.empresa.create import EmpresaCreateView
from core.representantetecnico.views.empresa.list import EmpresaListView
from core.representantetecnico.views.home import HomeView
from core.representantetecnico.views.inventario.list import InventarioListView
from core.representantetecnico.views.personas.create import PersonaCreateView
from core.representantetecnico.views.personas.delete import PersonasDeleteView
from core.representantetecnico.views.personas.list import PersonaListView
from core.representantetecnico.views.personas.update import PersonasUpdateView
from core.representantetecnico.views.repositorio.list import RepositorioListView
from core.representantetecnico.views.solicitudes.create import SustanciaCreateView
from core.representantetecnico.views.solicitudes.list import SolicitudListView
from core.representantetecnico.views.sustancia.list import SustanciaListView

app_name = "rp"

urlpatterns = [
    path('inventario/', SustanciaListView.as_view(), name="inventario"),
    path('inventario/movimientos/', InventarioListView.as_view(), name="movimientoinventario"),

    path('compras/', ComprasListView.as_view(), name="compras"),
    path('compras/registro/', ComprasCreateView.as_view(), name="registrocompras"),

    path('solicitudes/', SolicitudListView.as_view(), name="listadosolicitudes"),
    path('solicitudes/registro/', SustanciaCreateView.as_view(), name="entregasustancias"),

    path('empresas/', EmpresaListView.as_view(), name="empresas"),
    path('empresas/registro/', EmpresaCreateView.as_view(), name="registroempresa"),

    path('personas/', PersonaListView.as_view(), name="personas"),
    path('personas/registro/', PersonaCreateView.as_view(), name="registropersonas"),
    path('personas/update/<int:pk>/', PersonasUpdateView.as_view(), name="actualizacionpersonas"),
    path('personas/delete/<int:pk>/', PersonasDeleteView.as_view(), name="eliminarpersonas"),

    path('repositorio/', RepositorioListView.as_view(), name="repositorio"),
    path('repositorio/<int:pk>/', RepositorioListView.as_view(), name="repositorioid"),
]
