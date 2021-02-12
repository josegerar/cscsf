from django.urls import path

from core.login.views.login import LoginFormView
from core.login.views.logout import LogoutRedirectView

app_name = "session"

urlpatterns = [
    path('', LoginFormView.as_view(), name="login"),
    path('logout/', LogoutRedirectView.as_view(), name="logout")
]
