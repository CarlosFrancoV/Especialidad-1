from django.urls import path
from productos import views 
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

productos_urlpatterns =[
path('productos_producto_listar/',views.productos_producto_listar),
path('productos_producto_añadir/',views.productos_producto_añadir),
path('productos_producto_list_contains/',views.productos_producto_list_contains),
path('productos_categoria_listar/',views.productos_categoria_listar),
path('productos_categoria_añadir/',views.productos_categoria_añadir),
path('productos_categoria_list_contains/',views.productos_categoria_list_contains),
path('productos_producto_ver_info/',views.productos_producto_ver_info),
path('productos_editar_producto/',views.editar_producto),
path('productos_editar_categoria/',views.editar_categoria),
]