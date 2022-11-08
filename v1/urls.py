from django.urls import path
from v1 import views
from v1.views import *         
from django.conf.urls import url

v1_urlpatterns=[
    #templates
    path('', inicio.as_view(),name='casita'),
    path('vendedoract_list/',vendedoractlist.as_view(),name='vendedoract_list'),
    path('vendedorinac_list/', vendedorinaclist.as_view(),name='vendedorinac_list'),
    path('vendedor_add/', vendedoradd.as_view(),name='vendedor_add'),
    path('desactivar_ven/<int:pk>/', desactivarven.as_view(),name='desactivar_ven'),
    path('activar_ven/<int:pk>/', activarven.as_view(),name='activar_ven'),
    url(r'^editar/(?P<id_vendedor>\d+)/$',vendedor_edit, name='vendedor_edit'),
     #endpoints
    path('vendedores_vendedoract_list_rest/', views.vendedores_vendedoract_list_rest),
    path('vendedores_update_element_rest/', views.vendedores_update_element_rest),
    path('vendedores_add_rest/', views.vendedores_add_rest),
    path('vendedores_vendedoract_list_contains/',views.vendedores_vendedoract_list_contains),
    path('vendedores_vendedorinac_list_rest/',views.vendedores_vendedorinac_list_rest),
    path('vendedores_vendedorinac_list_contains/',views.vendedores_vendedorinac_list_contains),

]