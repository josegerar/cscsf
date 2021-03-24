from django.urls import path
from core.bodega.views.movimientosinventariobdg.list import MovimientosInventarioListViewbdg
from core.bodega.views.sustanciabdg.delete import SustanciaDeleteView
from core.bodega.views.sustanciabdg.list import SustanciaListView
from core.bodega.views.sustanciabdg.update import SustanciaUpdateView

app_name = "bdg"

urlpatterns = [
#invetanrio bodeguero
    path('movimientos/', MovimientosInventarioListViewbdg.as_view(), name="movimientoinventariobdg"),
    # sustancias
    path('sustancias/', SustanciaListView.as_view(), name="sustancias"),
    path('sustancias/update/<int:pk>/', SustanciaUpdateView.as_view(), name="actualizacionsustancia"),
    path('sustancias/delete/<int:pk>/', SustanciaDeleteView.as_view(), name="eliminarsustancia"),
]