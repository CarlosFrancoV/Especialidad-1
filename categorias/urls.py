from django.urls import path
from categorias import views
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
categorias_urlpatterns =[
path('main_categorias/',views.main_categorias,name="main_categorias"),
path('categorias_editar/',views.categorias_editar,name="categorias_editar"),
path('list_categorias/',views.list_categorias,name="list_categorias"),
path('categorias_add/',views.categorias_add,name="categorias_add"),
path('categorias_save/',views.categorias_save,name="categorias_save"),
path('categoria_listar/',views.categoria_listar),
path('categoria_listar_activas/',views.categoria_listar_activas),
path('categoria_añadir/',views.categoria_añadir),
path('categoria_list_contains/',views.categoria_list_contains),
path('categoria_editar_categoria/',views.categoria_editar_categoria),
]