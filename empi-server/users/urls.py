from django.urls import path
from .auth.views import LoginView, LogoutView, LogoutAllView

urlpatterns = [
    path(r"login/", LoginView.as_view(), name="knox_login"),
    path(r"logout/", LogoutView.as_view(), name="knox_logout"),
    path(r"logoutall/", LogoutAllView.as_view(), name="knox_logoutall"),
]
