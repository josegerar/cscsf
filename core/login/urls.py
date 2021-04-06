from django.urls import path

from core.login.views.login import LoginFormView
from core.login.views.logout import LogoutRedirectView
from core.login.views.recpass import recuperarpass
from core.login.views.recuser import recuperaruser

app_name = "session"

urlpatterns = [
    path('', LoginFormView.as_view(), name="login"),
    path('logout/', LogoutRedirectView.as_view(), name="logout"),
    path('recuperarpass/', recuperarpass.as_view(), name="recuperarpass"),
    path('recuperaruser/', recuperaruser.as_view(), name="recuperaruser")

]
