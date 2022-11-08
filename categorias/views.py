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
from categorias.models import Categoria
from django.db.models import Q

# Create your views here.

@login_required
def main_categorias(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'categorias/main_categorias.html'
    return render(request,template_name,{'profile':profile})

@login_required
def categorias_save(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    if request.method == 'POST':
        nombre = request.POST.get('nombre_categoria')
        if nombre == '':
            messages.add_message(request, messages.INFO, 'Debes ingresar toda la información')
            return redirect('categorias_add')
        categoria_save = Categoria(
            nombre_categoria=nombre,
            )
        categoria_save.save()
        messages.add_message(request, messages.INFO, 'Categoría ingresada con éxito')
        return redirect('list_categorias')
    else:
        messages.add_message(request, messages.INFO, 'Error en el método de envío')
        return redirect('check_group_main')

@login_required
def categorias_editar(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'categorias/categorias_editar.html'
    return render(request,template_name,{'profile':profile})


@login_required
def categorias_add(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'categorias/categorias_add.html'
    return render(request,template_name,{'profile':profile})

@login_required
def ejemplos_habilidad_ver(request,habilidad_id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    habildad_data = Categoria.objects.get(pk=habilidad_id)
    template_name = 'categorias/ejemplos_habilidad_ver.html'
    return render(request,template_name,{'profile':profile,'habildad_data':habildad_data})

@login_required
def list_categorias(request,page=None,search=None):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    if page == None:
        page = request.GET.get('page')
    else:
        page = page
    if request.GET.get('page') == None:
        page = page
    else:
        page = request.GET.get('page') 
    if search == None:
        search = request.GET.get('search')
    else:
        search = search
    if request.GET.get('search') == None:
        search = search
    else:
        search = request.GET.get('search') 
    if request.method == 'POST':
        search = request.POST.get('search') 
        page = None
    h_list = []
    if search == None or search == "None":
        h_count = Categoria.objects.filter(state='Activo').count()
        h_list_array = Categoria.objects.order_by('nombre_categoria')
        for h in h_list_array:
            h_list.append({'id':h.id,'nombre':h.nombre_categoria})    
    else:
        h_count = Categoria.objects.filter(state='Activo').filter(nombre_categoria__icontains=search).count()
        h_list_array = Categoria.objects.filter(state='Activo').filter(nombre_categoria__icontains=search).order_by('nombre_categoria')
        for h in h_list_array:
            h_list.append({'id':h.id,'nombre':h.nombre_categoria})        
    paginator = Paginator(h_list, 1) 
    h_list_paginate= paginator.get_page(page)   
    template_name = 'categorias/list_categorias.html'
    return render(request,template_name,{'template_name':template_name,'h_list_paginate':h_list_paginate,'paginator':paginator,'page':page})


#Listar Categorias
@api_view(['GET'])
def categoria_listar(request, format=None):
    if request.method=='GET':
        categoria_list = Categoria.objects.all().order_by('nombre_categoria')
        categoria_json = []
        for i in categoria_list:
            categoria_json.append({'Nombre Categoria':i.nombre_categoria})
        return Response({'Listado':categoria_json})
    else:
        return Response ({'Msj':"Error método no soportado"})

#Listar categorías activas
@api_view(['GET'])
def categoria_listar_activas(request, format=None):
    if request.method=='GET':
        categoria_list = Categoria.objects.filter(state='Activo').order_by('nombre_categoria')
        categoria_json = []
        for i in categoria_list:
            categoria_json.append({'Nombre Categoria':i.nombre_categoria,'Estado:':i.state})
        return Response({'Listado':categoria_json})
    else:
        return Response({'Msj':"Error metodo no soportado"})

#Añadir Categoria
@api_view(['POST'])
def categoria_añadir(request, format=None):
    if request.method=='POST':
        nombre= request.data['nombre_categoria']
        categoria_save=Categoria(
        nombre_categoria=nombre,
        )
        categoria_save.save()
        return Response({'Msj':"Categoria Creada"})
    else:
        return Response ({'Msj':"Error método no soportado"})

#Buscar Categoria
@api_view(['POST'])
def categoria_list_contains(request, format=None):
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
            return Response({'Msj':'No existen categorías que concuerden con la búsqueda realizada'})
    else:
        return Response({'Msj':'Error, método no soportado'})

#Editar Categoria
@api_view(['POST'])
def categoria_editar_categoria(request, format=None):
    if request.method=='POST':
        categoria_json = []
        categoria_id = request.data['categoria_id']
        nombre = request.data['nombre']
        estado = request.data['estado']
        Categoria.objects.filter(pk=categoria_id).update(nombre_categoria=nombre)
        Categoria.objects.filter(pk=categoria_id).update(state=estado)
        return Response ({'Msj':'Categoria editada con éxito'})
    else:
        return Response ({'Msj':'Error método no soportado'})