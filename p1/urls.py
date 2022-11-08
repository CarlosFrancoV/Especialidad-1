from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from p1 import views 

p1_urlpatterns=[
    #templates
    path('proveedores_main/',views.proveedores_main,name='proveedores_main'),
    path('proveedores_add/',views.proveedores_proveedores_add,name='proveedores_add'),
    path('proveedor_actlist_proveedores/',views.proveedor_actlist_proveedores,name='proveedor_actlist_proveedores'),
    path('proveedores_proveedor_save/',views.proveedores_proveedor_save,name='proveedores_proveedor_save'),
    path('proveedoredit/<id>/',views.proveedoredit, name='proveedoredit'),
    path('proveedor_inactlist_proveedores/',views.proveedor_inactlist_proveedores,name='proveedor_inactlist_proveedores'),
    
    #EndPoints
    path("proveedores_proveedoract_list_rest/",views.proveedores_proveedoract_list_rest),
    path("proveedores_update_element_rest/",views.proveedores_update_element_rest),
    path("proveedores_add_rest/",views.proveedores_add_rest),
    path("proveedores_proveedor_list_contains/",views.proveedores_proveedor_list_contains),
    path("proveedores_proveedorinac_list_contains/",views.proveedores_proveedorinac_list_contains),
    path("proveedores_proveedorinac_list_rest/",views.proveedores_proveedorinac_list_rest),
    
]
