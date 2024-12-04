from django.contrib import admin
from django.urls import path, include
from streaming import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('streaming.urls')),
    path('auth/', include('authentication.urls')),
    path("", views.home, name="home"),
]
