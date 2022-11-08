"""bussiness_solutions_dev_g2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.urls import core_urlpatterns
from p1.urls import p1_urlpatterns
from ordenescompra1.urls import ordenescompra1_urlpatterns
from v1.urls import v1_urlpatterns
from productos.urls import productos_urlpatterns
from ejemplos.urls import ejemplos_urlpatterns


urlpatterns = [
    path('',include(core_urlpatterns)),
    path('p1/', include(p1_urlpatterns)),
    path('v1/', include(v1_urlpatterns)),
    path('ordenescompra1/', include(ordenescompra1_urlpatterns)),
    path('productos/', include(productos_urlpatterns)),
    path('ejemplos/', include(ejemplos_urlpatterns)),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('registration.urls')),
    
]

admin.site.site_header = 'Administrador Bussiness_Solutions'
admin.site.site_title = 'bussinessSolutions'    

if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 


