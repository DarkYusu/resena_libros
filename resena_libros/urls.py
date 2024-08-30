"""resena_libros URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from aplicacion.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', inicio, name='inicio'),
    path('contacto/', contacto, name='contacto'),
    path('login/', login_view, name='login'),
    path('registro/', registro, name='registro'),
    path('logout/', logout_view, name='logout'),
    path('agendas/', agendas, name='agendas'),
    path('agenda/nuevo/', crear_agenda, name='crear_agenda'),  # Solo admin
    path('agenda/<int:id>/', detalle_agenda, name='detalle_agenda'),
    path('tipo_usuario/', seleccionar_tipo_usuario, name='seleccionar_tipo_usuario')
]
