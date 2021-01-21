from django.urls import path, include

app_name = "cssf"

urlpatterns = [
    path('rp/', include("CSSF.usurls.urls_rp")),
    path('tl/', include("CSSF.usurls.urls_tl")),
    path('bdg/', include("CSSF.usurls.urls_bdg"))
]