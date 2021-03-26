from django.urls import path

from core.tecnicolaboratorio.views.informes_mensuales.create import InformesMensualesCreateView
from core.tecnicolaboratorio.views.informes_mensuales.list import InformesMensualesListView
from core.tecnicolaboratorio.views.solicitudes.create import SolicitudCreateView
from core.tecnicolaboratorio.views.solicitudes.delete import SolicitudDeleteView
from core.tecnicolaboratorio.views.solicitudes.list import SolicitudListView
from core.tecnicolaboratorio.views.solicitudes.update import SolicitudUpdateView

app_name = "tl"

urlpatterns = [
    # solicitudes
    path('solicitudes/', SolicitudListView.as_view(), name="solicitudes"),
    path('solicitudes/registro/', SolicitudCreateView.as_view(), name="registrosolicitud"),
    path('solicitudes/update/<int:pk>/', SolicitudUpdateView.as_view(), name="actualizacionsolicitud"),
    path('solicitudes/delete/<int:pk>/', SolicitudDeleteView.as_view(), name="eliminarsolicitud"),

    # informes mensuales
    path('informes-mensuales/', InformesMensualesListView.as_view(), name="informesmensuales"),
    path('informes-mensuales/registro/', InformesMensualesCreateView.as_view(), name="registroinformesmensuales"),
    path('informes-mensuales/update/<int:pk>/', SolicitudUpdateView.as_view(), name="actualizacioninformesmensuales"),
    path('informes-mensuales/delete/<int:pk>/', SolicitudDeleteView.as_view(), name="eliminarinformesmensuales"),
]
