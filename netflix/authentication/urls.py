from django.urls import path
from .views import CustomLoginView, registrar, logout_view, mi_cuenta, UserProfileView

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("registrar/", registrar, name="register"),
    path("logout/", logout_view, name="logout"),
    path("mi_cuenta/", mi_cuenta, name="my_account"),
]