from django.urls import path

from core.representantetecnico.views.bodega.create import BodegaCreateView
from core.representantetecnico.views.bodega.delete import BodegaDeleteView
from core.representantetecnico.views.bodega.list import BodegaListView
from core.representantetecnico.views.bodega.update import BodegaUpdateView
from core.representantetecnico.views.compras.create import ComprasCreateView
from core.representantetecnico.views.compras.delete import ComprasDeleteView
from core.representantetecnico.views.compras.list import ComprasListView
from core.representantetecnico.views.compras.update import ComprasUpdateView
from core.representantetecnico.views.empresa.create import EmpresaCreateView
from core.representantetecnico.views.empresa.delete import EmpresaDeleteView
from core.representantetecnico.views.empresa.list import EmpresaListView
from core.representantetecnico.views.empresa.update import EmpresaUpdateView
from core.representantetecnico.views.laboratorio.create import LaboratorioCreateView
from core.representantetecnico.views.laboratorio.delete import LaboratorioDeleteView
from core.representantetecnico.views.laboratorio.list import LaboratorioListView
from core.representantetecnico.views.laboratorio.update import LaboratorioUpdateView
from core.representantetecnico.views.movimientosinventario.list import MovimientosInventarioListView
from core.representantetecnico.views.personas.create import PersonaCreateView
from core.representantetecnico.views.personas.delete import PersonasDeleteView
from core.representantetecnico.views.personas.list import PersonaListView
from core.representantetecnico.views.personas.update import PersonasUpdateView
from core.representantetecnico.views.repositorio.list import RepositorioListView
from core.representantetecnico.views.sustancia.create import SustanciaCreateView
app_name = "rp"

urlpatterns = [
    # bodega
    path('bodegas/', BodegaListView.as_view(), name="bodegas"),
    path('bodegas/registro/', BodegaCreateView.as_view(), name="registrobodega"),
    path('bodegas/update/<int:pk>/', BodegaUpdateView.as_view(), name="actualizacionbodega"),
    path('bodegas/delete/<int:pk>/', BodegaDeleteView.as_view(), name="eliminarbodega"),

    #sustancias
    path('sustancias/registro/', SustanciaCreateView.as_view(), name="registrosustancias"),

    # inventario
    path('inventario/movimientos/', MovimientosInventarioListView.as_view(), name="movimientoinventario"),

    # compras publicas
    path('compras/', ComprasListView.as_view(), name="compras"),
    path('compras/registro/', ComprasCreateView.as_view(), name="registrocompras"),
    path('compras/update/<int:pk>/', ComprasUpdateView.as_view(), name="actualizacioncompras"),
    path('compras/delete/<int:pk>/', ComprasDeleteView.as_view(), name="eliminarcompras"),

    # empresa
    path('empresas/', EmpresaListView.as_view(), name="empresas"),
    path('empresas/registro/', EmpresaCreateView.as_view(), name="registroempresa"),
    path('empresas/update/<int:pk>/', EmpresaUpdateView.as_view(), name="actualizacionempresa"),
    path('empresas/delete/<int:pk>/', EmpresaDeleteView.as_view(), name="eliminarempresa"),

    # investigadores
    path('investigadores/', PersonaListView.as_view(), name="personas"),
    path('investigadores/registro/', PersonaCreateView.as_view(), name="registropersonas"),
    path('investigadores/update/<int:pk>/', PersonasUpdateView.as_view(), name="actualizacionpersonas"),
    path('investigadores/delete/<int:pk>/', PersonasDeleteView.as_view(), name="eliminarpersonas"),

    # repositorio
    path('repositorio/', RepositorioListView.as_view(), name="repositorio"),
    path('repositorio/<int:pk>/', RepositorioListView.as_view(), name="repositorioid"),

    # laboratorio
    path('laboratorios/', LaboratorioListView.as_view(), name="laboratorios"),
    path('laboratorios/registro/', LaboratorioCreateView.as_view(), name="registrolaboratorio"),
    path('laboratorios/update/<int:pk>/', LaboratorioUpdateView.as_view(), name="actualizacionlaboratorios"),
    path('laboratorios/delete/<int:pk>/', LaboratorioDeleteView.as_view(), name="eliminarlaboratorio"),
]
