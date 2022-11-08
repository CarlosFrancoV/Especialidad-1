from ordenescompra1 import views
from django.contrib import admin
from django.urls import path,include
from ordenescompra1.views import *

ordenescompra1_urlpatterns=[
    #Templates
    path('', Index.as_view(),name='menu'),
    path('order_purchase_opcion/',OrdersPurchaseOpcion.as_view(),name='order_purchase_opcion'),
    path('list_order_purchase_pending/',OrdersPurchasePending.as_view(),name='list_order_purchase_pending'),
    path('list_order_purchase_sent/',OrdersPurchaseSent.as_view(),name='list_order_purchase_sent'),
    path('list_order_purchase_completed/',OrdersPurchaseCompleted.as_view(),name='list_order_purchase_completed'),
    path('list_order_purchase_canceled/',OrdersPurchaseCanceled.as_view(),name='list_order_purchase_canceled'),
    path('orders_pendant_edit/<int:pk>/',OrdersPendantEdit.as_view(),name='orders_pendant_edit'),
    path('orders_pendant_delete/<int:pk>/',OrdersPendantDelete.as_view(),name='orders_pendant_delete'),
    path('orders_pendant_change_state/<int:pk>/',OrdersPendantChangeState.as_view(),name='orders_pendant_change_state'),
    path('orders_sent_change_state_c/<int:pk>/',OrdersSentChangeStateCancelled.as_view(),name='orders_sent_change_state_c'),
    path('orders_sent_change_state_f/<int:pk>/',OrdersSentChangeStateFinalized.as_view(),name='orders_sent_change_state_f'),
    path('orders_sent_check/<int:pk>/',OrdersSentCheck.as_view(),name='orders_sent_check'),
    path('orders_purchase_info_finalized/<int:pk>/',OrdersInfoFinalized.as_view(),name='orders_purchase_info_finalized'),
    path('orders_purchase_info_all_orders/<int:pk>/',OrdersInfoAllOrders.as_view(),name='orders_purchase_info_all_orders'),
    path('orders_purchase_info_canceller/<int:pk>/',OrdersInfoCanceller.as_view(),name='orders_purchase_info_canceller'),
    path('products_critic_info/<int:pk>/',ProductsCriticsInfo.as_view(),name='products_critic_info'),
    path('list_order_purchase/', ListOrdersPurchase.as_view(),name='list_order_purchase'),
    path('list_products_critic/', ListProductsCritic.as_view(),name='list_products_critic'),
    path('create_order_purcharse/', CreateOrderPurchase.as_view(),name='create_order_purcharse'),
    #EndpointsClass----------
    path('products_list_details/', products_list_details,name='products_list_details'),
    path('order_purchase_all/',list_orders_purchase_all,name='order_purchase_all'),
    path('order_purchase_pending/',list_orders_purchase_pending,name='order_purchase_pending'),
    path('order_purchase_sent/',list_orders_purchase_sent,name='order_purchase_sent'),
    path('order_purchase_finalized/',list_orders_purchase_finalized,name='order_purchase_finalized'),
    path('order_purchase_canceller/',list_orders_purchase_canceller,name='order_purchase_canceller'),
    path('order_purchase_details/<int:pk>/',details_orders_purchase,name='order_purchase_details'),
    path('orders_purchase_state_sent/<int:pk>/',orders_purchase_state_sent,name='orders_purchase_state_sent'),
    path('orders_purchase_state_canceller/<int:pk>/',orders_purchase_state_canceller,name='orders_purchase_state_canceller'),
    path('orders_purchase_state_finalized/<int:pk>/',orders_purchase_state_finalized,name='orders_purchase_state_finalized'),
    #Endpoints
    path('ordenesdecompra_ordendecompra_list_rest/',views.ordenesdecompra_ordendecompra_list_rest),
    path('ordenesdecompra_update_element_rest/',views.ordenesdecompra_update_element_rest),
    path('ordenesdecompra_del_element_rest/',views.ordenesdecompra_del_element_rest),
    path('ordenesdecompra_list_contains/',views.ordenesdecompra_list_contains),
    path('ordenesdecompra_list_range_date_rest/',views.ordenesdecompra_list_range_date_rest),
    path("listaproveedores_list_rest/",views.listaproveedores_list_rest),
    path("buscar_historial_list_contains/",views.buscar_historial_list_contains),
    path("listarhistorial_list_rest/",views.listarhistorial_list_rest),
    path("historial_pedidos_list_range_date_rest/",views.historial_pedidos_list_range_date_rest),
    path("crear_orden_compra_add_rest/",views.crear_orden_compra_add_rest),

]