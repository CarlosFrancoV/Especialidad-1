import json
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from registration.models import Profile
from xml.etree.ElementTree import QName
from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.decorators import (api_view, authentication_classes, permission_classes)
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from productos.models import Producto
from productos.models import Categoria
from django.db.models import Q
# Create your views here.

#Guardar datos
@api_view(['POST'])
def productos_producto_añadir(request, format=None):
    if request.method == 'POST':
        nombre = request.data['nombre_producto']
        sku = request.data['sku_producto']
        codigo =request.data['codigo_barras_producto']
        precio = request.data['precio_producto']
        costo =request.data['costo_producto']
        stock= request.data['stock_producto']
        stockpromedio = request.data['stock_promedio']
        if nombre == '' or sku == '' or codigo =='' or precio =='' or costo =='':
            return Response({'Msj':"Error, los campos no pueden estar vacios"})
        producto_save=Producto(
            nombre_producto=nombre,
            sku_producto=sku,
            codigo_barras_producto=codigo,
            precio_producto=precio,
            costo_producto=costo,     
            stock_producto=stock,   
            stock_promedio=stockpromedio,
        )    
        producto_save.save()
        return Response({'Msj':"Producto Creado"})
    else:
        return Response({'Msj':"Error, metodo no soportado"})

#Listar Datos
@api_view(['GET'])
def productos_producto_listar(request, format=None):
    if request.method=='GET':
        producto_list = Producto.objects.all().order_by('nombre_producto')
        producto_json = []
        for i in producto_list:
            producto_json.append({'Nombre':i.nombre_producto,'SKU':i.sku_producto,'Codigo':i.codigo_barras_producto,'Precio':i.precio_producto,'Costo':i.costo_producto,'Stock':i.stock_producto})
        return Response({'Listado':producto_json})
    else:
        return Response({'Msj':"Error metodo no soportado"})

#Buscar productos
@api_view(['POST'])
def productos_producto_list_contains(request, format=None):
    if request.method == 'POST':
        search = request.data['search']
        producto_list_count = Producto.objects.filter(
            Q(nombre_producto__icontains=search)|
            Q(sku_producto__icontains=search)|
            Q(codigo_barras_producto__icontains=search))
        if producto_list_count.count() > 0:
            producto_list = Producto.objects.filter(Q(nombre_producto__icontains=search)|Q(sku_producto__icontains=search)|Q(codigo_barras_producto__icontains=search))
            producto_json = []
            for i in producto_list:
                    producto_json.append({'producto':i.nombre_producto,'sku':i.sku_producto,'codigo de barras':i.codigo_barras_producto})
            return Response({'Listado':producto_json})
        else:
            return Response({'Msj':'No existen productos que concuerden con la búsqueda realizada'})
    else:
        return Response({'Msj':'Error, método no soportado'})

#Lustar Categorias
@api_view(['GET'])
def productos_categoria_listar(request, format=None):
    if request.method=='GET':
        categoria_list = Categoria.objects.all().order_by('nombre_categoria')
        categoria_json = []
        for i in categoria_list:
            categoria_json.append({'Nombre Categoria':i.nombre_categoria,})
        return Response({'Listado':categoria_json})
    else:
        return Response ({'Msj':"Error metodo no soportado"})

#Añadir Categoria
@api_view(['POST'])
def productos_categoria_añadir(request, format=None):
    if request.method=='POST':
        nombre= request.data['nombre_categoria']
        categoria_save=Categoria(
        nombre_categoria=nombre,
        )
        categoria_save.save()
        return Response({'Msj':"Categoria Creada"})
    else:
        return Response ({'Msj':"Error.metodo no soportado"})


#Buscar Categoria
@api_view(['POST'])
def productos_categoria_list_contains(request, format=None):
    if request.method == 'POST':
        search = request.data['search']
        Categoria_list_count = Categoria.objects.filter(Q(nombre_categoria__icontains=search))
        if Categoria_list_count.count() > 0:
            categoria_list = Categoria.objects.filter(Q(nombre_categoria__icontains=search))
            categoria_json = []
            for i in categoria_list:
                categoria_json.append({'categoria':i.nombre_categoria})
            return Response({'Listado':categoria_json})
        else:
            return Response({'Msj':'No existen categoria que concuerden con la búsqueda realizada'})
    else:
        return Response({'Msj':'Error, método no soportado'})

#Ver información producto
@api_view(['POST'])
def productos_producto_ver_info(request, format=None):
    if request.method == 'POST':
        producto_json = []
        id_producto = request.data['id']
        producto_array = Producto.objects.get(pk=id_producto)
        producto_json.append(
            {'nombre':producto_array.nombre_producto,
             'sku':producto_array.sku_producto,
             'codigo de barras':producto_array.codigo_barras_producto})
        return Response({producto_array.nombre_producto:producto_json})
    else:
        return Response({'Msj: Error, método no soportado'})

#editar producto
@api_view(['POST'])
def editar_producto(request, format=None):
    if request.method=='POST':
        producto_json = []
        producto_id = request.data['producto_id']
        nombre = request.data['nombre']
        precio =request.data['precio_producto']
        costo =request.data['costo_producto']
        stock =request.data['stock']
        estado=request.data['estado']
        Producto.objects.filter(pk=producto_id).update(nombre_producto=nombre)
        Producto.objects.filter(pk=producto_id).update(precio_producto=precio)
        Producto.objects.filter(pk=producto_id).update(costo_producto=costo)
        Producto.objects.filter(pk=producto_id).update(stock_producto=stock)
        Producto.objects.filter(pk=producto_id).update(state=estado)
        return Response ({'Msj':'Producto editado con exito'})
    else:
        return Response ({'Msj':'Error metodo no soportado'})

#Editar Categoria
@api_view(['POST'])
def editar_categoria(request, format=None):
    if request.method=='POST':
        categoria_json = []
        categoria_id = request.data['categoria_id']
        nombre = request.data['nombre']
        estado = request.data['estado']
        Categoria.objects.filter(pk=categoria_id).update(nombre_categoria=nombre)
        Categoria.objects.filter(pk=categoria_id).update(state=estado)
        return Response ({'Msj':'Categoria editada con exito'})
    else:
        return Response ({'Msj':'Error metodo no soportado'})
