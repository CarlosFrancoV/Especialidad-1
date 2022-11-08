import io
import json
from os import name
from sre_constants import SUCCESS
from urllib import response
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.urls import reverse_lazy
from registration.models import Profile
from django.shortcuts import render
from django.db.models import CharField
from rest_framework import generics, viewsets
from rest_framework.decorators import (api_view, authentication_classes, permission_classes)
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
import sys
from itertools import cycle
from ordenescompra1.models import *
from p1.models import *
from v1.models import *
from productos.models import *
from django.db.models import Q
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from .forms import Ordencompra1Form,ProductsForm
from .serializers import Ordencompra1Serializer,ProductsDetailsSerializer,Ordencompra1SerializerEdit,Ordencompra1SerializerCreate,Ordencompra1SerializerChangeState
import random

# Create your views here.
class CreateOrderPurchase(CreateView):
    model=Ordencompra1
    fields = '__all__'
    form_class: Ordencompra1Form
    template_name='create_order_purcharse.html'
    success_url = reverse_lazy('list_order_purchase_pending')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creacion orden de compra'
        return context
    
"""     def post(self,request,*args,**kwargs):
        object = Ordencompra1.objects.all()
        object.numero_pedido = random.randint(100,999)
        return redirect('list_order_purchase_pending') """


class OrdersPurchaseOpcion(ListView):
    model=Ordencompra1
    template_name='order_purchase_opcion.html'

class OrdersPurchaseInfoFinalized(ListView):
    model=Ordencompra1
    template_name='orders_purchase_info_finalized.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Info ordenes de compra finalizadas'
        return context

class OrdersPurchasePending(ListView):
    model=Ordencompra1
    template_name='list_orders_purchase_p.html'

    def get_queryset(self):
        return Ordencompra1.objects.filter(estado_pedido__startswith='Pendiente')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de ordenes pendientes'
        return context

class OrdersPurchaseSent(ListView):
    model=Ordencompra1
    template_name='list_orders_purchase_e.html'

    def get_queryset(self):
        return Ordencompra1.objects.filter(estado_pedido__startswith='Enviado')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de ordenes enviadas'
        return context

class OrdersPurchaseCompleted(ListView):
    model=Ordencompra1
    template_name='list_orders_purchase_f.html'

    def get_queryset(self):
        return Ordencompra1.objects.filter(estado_pedido__startswith='Finalizado')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de ordenes finalizadas'
        return context

class OrdersPurchaseCanceled(ListView):
    model=Ordencompra1
    template_name='list_orders_purchase_c.html'

    def get_queryset(self):
        return Ordencompra1.objects.filter(estado_pedido__startswith='Cancelado')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de ordenes Canceladas'
        return context

class ProductsCriticsInfo(UpdateView):
    model=Producto
    fields = '__all__'
    form_class: ProductsForm
    template_name='products_critic_info.html'
    success_url = reverse_lazy('list_products_critic')

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Detalles de Prodcuto critico'
        return context

class OrdersPendantEdit(UpdateView):
    model=Ordencompra1
    fields = ('cantidad_orden','precio_orden')
    form_class: Ordencompra1Form
    template_name='orders_pendant_edit.html'
    success_url = reverse_lazy('list_order_purchase_pending')

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'editar orden pendiente'
        context['list_url'] = reverse_lazy('list_order_purchase_sent')
        context['action'] = 'edit'
        return context

class OrdersInfoFinalized(UpdateView):
    model=Ordencompra1
    fields = ('cantidad_orden','precio_orden')
    form_class: Ordencompra1Form
    template_name='orders_purchase_info_finalized.html'
    success_url = reverse_lazy('list_order_purchase_sent')

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Detalles de ordenes de compra'
        return context

class OrdersInfoCanceller(UpdateView):
    model=Ordencompra1
    fields = ('cantidad_orden','precio_orden')
    form_class: Ordencompra1Form
    template_name='orders_purchase_info_canceller.html'
    success_url = reverse_lazy('list_order_purchase_sent')

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Detalles de ordenes de compra'
        return context

class OrdersInfoAllOrders(UpdateView):
    model=Ordencompra1
    fields = ('cantidad_orden','precio_orden')
    form_class: Ordencompra1Form
    template_name='orders_purchase_info_all_orders.html'
    success_url = reverse_lazy('list_order_purchase_sent')

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Detalles de ordenes de compra'
        return context

class OrdersSentCheck(UpdateView):
    model=Ordencompra1
    fields = ('cantidad_orden','precio_orden')
    form_class: Ordencompra1Form
    template_name='orders_sent_check.html'
    success_url = reverse_lazy('list_order_purchase_sent')

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'editar orden pendiente'
        context['list_url'] = reverse_lazy('list_order_purchase_sent')
        context['action'] = 'edit'
        return context

class ListOrdersPurchase(ListView):
    model=Ordencompra1
    template_name='list_orders_purchase.html'

class ListProductsCritic(ListView):
    model=Producto
    template_name='list_critical_products.html'

class Index(ListView):
    model=Producto
    template_name='index.html'


class OrdersPendantDelete(DeleteView):
    model=Ordencompra1
    template_name='orders_pendant_delete.html'
    success_url = reverse_lazy('list_order_purchase_sent')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'eliminacion de una categoria'
        context['list_url'] = reverse_lazy('list_order_purchase_sent')
        return context

class OrdersPendantChangeState(DeleteView):
    model=Ordencompra1
    template_name='orders_pendant_change_state.html'

    def post(self,request,pk,*args,**kwargs):
        object = Ordencompra1.objects.get(id = pk)
        object.estado_pedido = 'Enviado'
        object.save()
        return redirect('list_order_purchase_sent')

class OrdersSentChangeStateFinalized(DeleteView):
    model=Ordencompra1
    template_name='orders_sent_change_state_f.html'

    def post(self,request,pk,*args,**kwargs):
        object = Ordencompra1.objects.get(id = pk)
        object.estado_pedido = 'Finalizado'
        object.save()
        return redirect('list_order_purchase_sent')

class OrdersSentChangeStateCancelled(DeleteView):
    model=Ordencompra1
    template_name='orders_sent_change_state_c.html'

    def post(self,request,pk,*args,**kwargs):
        object = Ordencompra1.objects.get(id = pk)
        object.estado_pedido = 'Cancelado'
        object.save()
        return redirect('list_order_purchase_sent')


# ************************************** API **********************************************

@api_view(['GET'])
def products_list_details(request):

    if request.method == 'GET':
        productos = Producto.objects.all()
        producto_serializer = ProductsDetailsSerializer(productos,many = True)
        return Response(producto_serializer.data)


@api_view(['GET','POST'])
def list_orders_purchase_all(request):

    if request.method == 'GET':
        ordencompra1 = Ordencompra1.objects.all()
        order_serializer = Ordencompra1Serializer(ordencompra1,many = True)
        return Response(order_serializer.data)
    
    elif request.method == 'POST':
        order_details_serializer = Ordencompra1SerializerCreate(data=request.data)
        if order_details_serializer.is_valid():
            order_details_serializer.save()
            return Response(order_details_serializer.data)
        return Response(order_details_serializer.errors)

@api_view(['GET'])
def list_orders_purchase_pending(request):

    if request.method == 'GET':
        ordencompra1 = Ordencompra1.objects.all().filter(estado_pedido = "Pendiente")
        order_pending_serializer = Ordencompra1Serializer(ordencompra1,many = True)
        return Response(order_pending_serializer.data)

@api_view(['GET'])
def list_orders_purchase_sent(request):

    if request.method == 'GET':
        ordencompra1 = Ordencompra1.objects.all().filter(estado_pedido = "Enviado")
        order_sent_serializer = Ordencompra1Serializer(ordencompra1,many = True)
        return Response(order_sent_serializer.data)

@api_view(['GET'])
def list_orders_purchase_finalized(request):

    if request.method == 'GET':
        ordencompra1 = Ordencompra1.objects.all().filter(estado_pedido = "Finalizado")
        order_finalized_serializer = Ordencompra1Serializer(ordencompra1,many = True)
        return Response(order_finalized_serializer.data)

@api_view(['GET'])
def list_orders_purchase_canceller(request):

    if request.method == 'GET':
        ordencompra1 = Ordencompra1.objects.all().filter(estado_pedido = "Cancelado")
        order_canceller_serializer = Ordencompra1Serializer(ordencompra1,many = True)
        return Response(order_canceller_serializer.data)

@api_view(['GET','PUT','DELETE'])
def details_orders_purchase(request,pk=None):

    if request.method == 'GET':
        ordencompra1 = Ordencompra1.objects.filter(id=pk).first()
        order_details_serializer = Ordencompra1Serializer(ordencompra1)
        return Response(order_details_serializer.data)
    
    elif request.method == 'PUT':
        ordencompra1 = Ordencompra1.objects.filter(id=pk).first()
        order_details_serializer = Ordencompra1SerializerEdit(ordencompra1,data=request.data)
        if order_details_serializer.is_valid():
            order_details_serializer.save()
            return Response(order_details_serializer.data)
        return Response(order_details_serializer.errors)
    
    elif request.method == 'DELETE':
        ordencompra1 = Ordencompra1.objects.filter(id=pk).first()
        ordencompra1.delete()
        return Response('Eliminado')

@api_view(['PUT'])
def orders_purchase_state_sent(request,pk=None):
    if request.method == 'PUT':
        ordencompra1 = Ordencompra1.objects.filter(id=pk).first()
        estado2 = {
                    "estado_pedido": "Enviado"
                }
        
        order_details_serializer = Ordencompra1SerializerChangeState(ordencompra1,data=estado2)
        if order_details_serializer.is_valid():
            order_details_serializer.save()
            return Response(order_details_serializer.data)
        return Response(order_details_serializer.errors)

@api_view(['PUT'])
def orders_purchase_state_canceller(request,pk=None):
    if request.method == 'PUT':
        ordencompra1 = Ordencompra1.objects.filter(id=pk).first()
        estado2 = {
                    "estado_pedido": "Cancelado"
                }
        
        order_details_serializer = Ordencompra1SerializerChangeState(ordencompra1,data=estado2)
        if order_details_serializer.is_valid():
            order_details_serializer.save()
            return Response(order_details_serializer.data)
        return Response(order_details_serializer.errors)

@api_view(['PUT'])
def orders_purchase_state_finalized(request,pk=None):
    if request.method == 'PUT':
        ordencompra1 = Ordencompra1.objects.filter(id=pk).first()
        estado2 = {
                    "estado_pedido": "Finalizado"
                }
        
        order_details_serializer = Ordencompra1SerializerChangeState(ordencompra1,data=estado2)
        if order_details_serializer.is_valid():
            order_details_serializer.save()
            return Response(order_details_serializer.data)
        return Response(order_details_serializer.errors)



#grupo2
#Listar Ordenes de Compra
@api_view(['GET'])
def ordenesdecompra_ordendecompra_list_rest(request, format=None):
    if request.method == 'GET':
        ordencompra1_list = Ordencompra1.objects.all()
        proveeedores_list = P1.objects.all().order_by('nombre_proveedor')
        prov = P1.objects.get(pk=id)
        vend_list = V1.objects.all().order_by('nombre_vendedor')
        ordencompra1_json = []
        if ordencompra1_list.filter(estado_pedido ='P').exists():
            for h in ordencompra1_list.filter(estado_pedido ='P'):
                for i in proveeedores_list:
                    for j in vend_list:
                        ordencompra1_json.append({
                            'Numero de orden':h.numero_pedido,
                            'Proveedor':i.nombre_proveedor,
                            'Prov':prov.nombre_proveedor,
                            'Estado':h.estado_pedido,
                            'Creado':h.created,
                            'Cantidad':h.cantidad_orden,
                            'Precio de la orden':h.precio_orden,
                            'Vendedor':j.nombre_vendedor,
                            'producto':h.created
                            })
            return Response({'Listado':ordencompra1_json})
        else:
            return Response({'Msj':"No se encuentran ordenes activas"})    
    else:
        return Response({'Msj':"Error método no soportado"})



#Editar orden de compra
@api_view(['POST'])
def ordenesdecompra_update_element_rest(request, format=None):
    if request.method == 'POST':
        ordencompra1_json = []
        ordencompra1_id = request.data['ordendecompra_id']
        cantidad = request.data['precio_orden']
        precio = request.data['cantidad_orden']
        ordencompra1.objects.filter(pk=Ordencompra1_id).update(precio_orden=cantidad)
        ordencompra1.objects.filter(pk=Ordencompra1_id).update(cantidad_orden=precio)
        return Response({'Msj':'Orden de compra editada con éxito'})
    else:
        return Response({'Msj':"Error, método no soportado."})

#Eliminar orden de compra
@api_view(['POST'])
def ordenesdecompra_del_element_rest(request, format=None):
    if request.method == 'POST':
        ordencompra1_json = []
        ordencompra1_id = request.data['ordendecompra_id']
        ordencompra1.objects.filter(pk=Ordencompra1_id).delete()
        return Response({'Msj':'Orden de Compra eliminada con éxito'})
    else:
        return Response({'Msj':"Error, método no soportado."})


#Buscar orden de compra
@api_view(['POST'])
def ordenesdecompra_list_contains(request, format=None):
    if request.method == 'POST':
        search = request.data['search']
        ordenescompra_list_count = Ordencompra1.objects.filter(Q(proveedor__nombre_proveedor__icontains=search)|Q(estado_pedido__icontains=search)|Q(numero_pedido__icontains=search)).exists()
        if ordenescompra_list_count > 0:
            ordenescompra_list = Ordencompra1.objects.filter(Q(proveedor__nombre_proveedor__icontains=search)|Q(estado_pedido__icontains=search)|Q(numero_pedido__icontains=search))
            ordenescompra_json = []
            for h in ordenescompra_list:
                ordenescompra_json.append({'Proveedor':h.proveedor.nombre_proveedor,'Numero de pedido':h.numero_pedido,'Estado':h.estado_pedido})
            return Response({'Listado': ordenescompra_json})
        else:
            return Response({'Msj':'No existen proveedores Activos que concuerden'})
    else:
        return Response({'Msj':'Error método no soportado'})


#Buscar por rango fecha orden de compra
@api_view(['POST'])
def ordenesdecompra_list_range_date_rest(request, format=None):
    if request.method == 'POST':
        initial = request.data['initial']
        final = request.data['final']
        ordencompra1_list_count = Ordencompra1.objects.filter(created__range=(initial,final)).count()
        if ordencompra1_list_count > 0:
            ordencompra1_list =Ordencompra1.objects.filter(created__range=(initial,final)).order_by('nombre_proveedor')
            ordencompra1_json = []
            for h in ordencompra1_list:
                ordencompra1_json.append({'Estado Pedido':h.estado_pedido,'Numero pedido':h.numero_pedido})
            return Response({'Listado': ordencompra1_json})
        else:
            return Response({'Msj':'No existen ordenes creadas entre el '+str(initial)+' al '+str(final)})
    else:
        return Response({'Msj':'Error método no soportado'})




#grupo1

##ORDENES DE COMPRA 
#LISTAR PROVEEDORES
@api_view(['GET'])
def listaproveedores_list_rest(request, format=None):
    if request.method == 'GET':
        listaproveedores_list = P1.objects.all().order_by('nombre_proveedor')
        listaproveedores_json = []
        if listaproveedores_list.filter(estado_proveedor ='Activo').exists():
            for h in listaproveedores_list.filter(estado_proveedor ='Activo'):
                listaproveedores_json.append({'Proveedor':h.nombre_proveedor,})
            return Response({'Listado':listaproveedores_json})
        else:
            return Response({'Msj':"No se encuentran Proveedores Activos"})
    else:
        return Response({'Msj':"Error metodo no soportado"})

##ORDENES DE COMPRA
#CREAR ORDEN DE COMPRA 
@api_view(['POST'])
def crear_orden_compra_add_rest(request, format=None):
    if request.method == 'POST':
        numero_pedido = random.randint(100,999)
        id_vendedor = request.data['id vendedor']
        id_proveedor = request.data['id proveedor']
        id_producto = request.data['id producto']
        cantidad_orden = request.data['cantidad de orden']
        precio_orden = request.data['precio orden']
        if Ordencompra1.objects.filter(numero_pedido=numero_pedido):
            return Response ({'Msj' : "Este numero de pedido ya existe"})
        if id_proveedor == '' or id_producto == '' or cantidad_orden == '' or precio_orden == '' :
            return Response ({'Msj' : "Error los datos no pueden estar en blanco"})
        ordencompra1_save = Ordencompra1(
            numero_pedido= numero_pedido,
            proveedor_id = id_proveedor,
            producto_id = id_producto,
            cantidad_orden = cantidad_orden,
            precio_orden =precio_orden,
            vendedor_id = id_vendedor,
            )
        ordencompra1_save.save()
        return Response ({'Msj' : "Orden de compra creada"})
    else:
        return Response ({'Msj' : "Error metodo no soportado"})




##HISTORIAL
#BUSCAR EN HISTORIAL 
@api_view(['POST'])
def buscar_historial_list_contains(request, format=None):
    if request.method == 'POST':
        historialbus_list = Ordencompra1.objects.all().order_by('numero_pedido')
        search = request.data['search']
        historialbus_list_count = Ordencompra1.objects.filter(Q(proveedor__nombre_proveedor__icontains=search)|Q(proveedor__dato_vendedor__nombre_vendedor__icontains=search)|Q(numero_pedido__icontains=search)|Q(cantidad_orden__icontains=search)).count()
        if historialbus_list_count > 0:
            historialbus_list = Ordencompra1.objects.filter(Q(proveedor__nombre_proveedor__icontains=search)|Q(proveedor__dato_vendedor__nombre_vendedor__icontains=search)|Q(numero_pedido__icontains=search)|Q(cantidad_orden__icontains=search))
            historialbus_json = []
            for h in historialbus_list:
                historialbus_json.append({'Proveedor':h.proveedor.nombre_proveedor,'Vendedor':h.proveedor.dato_vendedor.nombre_vendedor ,'Producto':h.producto.nombre_producto ,'Numero de pedido':h.numero_pedido,'Cantidad':h.cantidad_orden,'Precio':h.precio_orden})
            return Response({'Listado': historialbus_json})
        else:
            return Response({'Msj':'No existen ordenes de compra con parametros de busqueda que concuerden'})
    else:
        return Response({'Msj':'Error método no soportado'}) 


##HISTORIAL
#LISTAR HISTORIAL DE PEDIDO 
@api_view(['GET'])
def listarhistorial_list_rest(request, format=None):
    if request.method == 'GET':
        listarhistorial_list = Ordencompra1.objects.all().order_by('proveedor')
        listarhistorial_json = []
        for h in listarhistorial_list:
            listarhistorial_json.append({'Numero de pedido':h.numero_pedido,'Proveedor':h.proveedor.nombre_proveedor,'Vendedor':h.proveedor.dato_vendedor.nombre_vendedor ,'Cantidad':h.cantidad_orden,'Precio':h.precio_orden})
        return Response({'Listado':listarhistorial_json})
    else:
        return Response({'Msj':"Error metodo no soportado"})


##HISTORIAL
#FILTRAR HISToRIAL DE PEDIDOS POR RANGOS DE FECHA 
@api_view([ 'POST' ])
def historial_pedidos_list_range_date_rest(request, format=None):
    if request.method =='POST':
        initial = request.data['initial']
        final = request.data['final']
        historial_list_count = Ordencompra1.objects.filter(created__range=(initial,final)).count()
        if historial_list_count > 0:
            historial_list = Ordencompra1.objects.filter(created__range=(initial,final)).order_by('numero_pedido')
            historial_json = []
            for h in historial_list:
                historial_json.append({'Numero de pedido':h.numero_pedido,'Proveedor':h.proveedor.nombre_proveedor ,'Vendedor':h.proveedor.dato_vendedor.nombre_vendedor ,'Cantidad':h.cantidad_orden,'Precio':h.precio_orden})
            return Response({'Listado': historial_json})
        else:
                return Response({'Msj": "No existen ordenes de compra realizadas entre el '+str(initial)+' al '+str(final)})
    else:
        return Response ({'Msj':'Error método no soportado'})


