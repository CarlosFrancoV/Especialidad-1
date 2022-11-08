import json
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from registration.models import Profile
from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.decorators import (api_view, authentication_classes, permission_classes)
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.urls import reverse_lazy
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
import sys
from itertools import cycle
from p1.models import *
from django.db.models import Count, Avg, Q
from p1.forms import *
from productos.models import *


# Create your views here.

#EndPoints
def validarRut(rut):
	rut = rut.upper()
	rut = rut.replace("-","")
	rut = rut.replace(".","")
	aux = rut[:-1]
	dv = rut[-1:]
	revertido = map(int, reversed(str(aux)))
	factors = cycle(range(2,8))
	s = sum(d * f for d, f in zip(revertido,factors))
	res = (-s)%11
	if str(res) == dv:
		return True
	elif dv=="K" and res==10:
		return True
	else:
		return False


#Guardar proveedores
@api_view(['POST'])
def proveedores_add_rest(request, format=None):
    if request.method == 'POST':
        nombre = request.data['nombre']
        rut = request.data['rut']
        telefono = request.data['telefono']
        correo = request.data['correo']
        direccion = request.data['direccion']
        id_producto = request.data['id_producto']
        validarRut(rut)
        if validarRut(rut)==True:
            if P1.objects.filter(rut_proveedor=rut):
                return Response({'Msj':"Este rut ya se encuentra registrado"})
            else:
                if nombre == '' or rut == '' or telefono == '' or correo == '' or direccion == '' or id_producto == '' :
                    return Response({'Msj': "Error, los datos no pueden estar en blanco"})
            
            proveedor_save = P1(
            nombre_proveedor = nombre,
            rut_proveedor = rut,
            telefono_proveedor = telefono,
            correo_proveedor = correo,
            direccion_proveedor = direccion,
            )
            proveedor_save.save()
            proveedor_save.dato_producto.add(id_producto)
            return Response({'Msj':"Proveedor creado"})    
        else:
            return Response({'Msj':"Ingrese rut valido"})    
    else:
        return Response ({'Msj':"Error, método no soportado"})


#Activar y Desactivar Proveedores
@api_view(['POST'])
def proveedores_update_element_rest(request, format=None):
    if request.method == 'POST':
        proveedor_json = []
        proveedor_id = request.data['proveedor_id']
        estado = request.data['estado']
        if (estado != "Activo") and (estado != "Inactivo"):
            return Response ({'Msj':'formato de estado incorrecto, porfavor ingrese un estado valido, ej: Activo o Inactivo'})
        else:
            P1.objects.filter(pk=proveedor_id).update(estado_proveedor=estado)
        return Response({'Msj':'Estado modificado con éxito'})
    else:
        return Response({'Msj':"Error, método no soportado."})



#Listar Proveedores Activos
@api_view(['GET'])
def proveedores_proveedoract_list_rest(request, format=None):
    if request.method == 'GET':
        proveedor_list = P1.objects.all().order_by('nombre_proveedor')
        proveedor_json = []
        if proveedor_list.filter(estado_proveedor ='Activo').exists():
            for h in proveedor_list.filter(estado_proveedor ='Activo'):
                proveedor_json.append({'id de Prov':h.id,'Prov':h.nombre_proveedor,'RUT':h.rut_proveedor,'Correo':h.correo_proveedor,'Telefono':h.telefono_proveedor,'Direccion':h.direccion_proveedor,'Estado':h.estado_proveedor})
            return Response({'Listado':proveedor_json})
        else:
            return Response({'Msj':"No se encuentran Proveedores activos"})    
    else:
        return response({'Msj':"Error método no soportado"})

#Listar Proveedores Inactivos
@api_view(['GET'])
def proveedores_proveedorinac_list_rest(request, format=None):
    if request.method == 'GET':
        proveedor_list = P1.objects.all().order_by('nombre_proveedor')
        proveedor_json = []
        if proveedor_list.filter(estado_proveedor ='Inactivo').exists():
            for h in proveedor_list.filter(estado_proveedor ='Inactivo'):
                proveedor_json.append({'id de Porveedor':h.id,'Prov':h.nombre_proveedor,'RUT':h.rut_proveedor,'Correo':h.correo_proveedor,'Telefono':h.telefono_proveedor,'Direccion':h.direccion_proveedor,'Estado':h.estado_proveedor})
            return Response({'Listado':proveedor_json})
        else:
            return Response({'Msj':"No se encuentran Proveedores Inactivos"})    
    else:
        return response({'Msj':"Error método no soportado"})  


#Buscar Proveedores Activos
@api_view(['POST'])
def proveedores_proveedor_list_contains(request, format=None):
    if request.method == 'POST':
        proveedor_list = P1.objects.all().order_by('nombre_proveedor')
        search = request.data['search']
        proveedor_list_count = P1.objects.filter(Q(nombre_proveedor__icontains=search)|Q(rut_proveedor=search)).count()
        if proveedor_list_count > 0:
            proveedor_list = P1.objects.filter(Q(nombre_proveedor__icontains=search)|Q(rut_proveedor=search))
            proveedor_json = []
            if proveedor_list.filter(estado_proveedor ='Activo').exists():
                for h in proveedor_list.filter(estado_proveedor ='Activo'):
                    proveedor_json.append({'id de Prov':h.id,'Prov':h.nombre_proveedor,'RUT':h.rut_proveedor,'Correo':h.correo_proveedor,'Telefono':h.telefono_proveedor,'Direccion':h.direccion_proveedor,'Estado':h.estado_proveedor})
                    return Response({'Listado': proveedor_json})
            else:
                return Response({'Msj':'No se encuentran Proveedores activos que concuerden'})    
        else:
            return Response({'Msj':'No existen Proveedores Activos que concuerden'})
    else:
        return Response({'Msj':'Error método no soportado'})     



#Buscar Proveedores Inactivos
@api_view(['POST'])
def proveedores_proveedorinac_list_contains(request, format=None):
    if request.method == 'POST':
        proveedor_list = P1.objects.all().order_by('nombre_proveedor')
        search = request.data['search']
        proveedor_list_count = P1.objects.filter(Q(nombre_proveedor__icontains=search)|Q(rut_proveedor=search)).count()
        if proveedor_list_count > 0:
            proveedor_list = P1.objects.filter(Q(nombre_proveedor__icontains=search)|Q(rut_proveedor=search))
            proveedor_json = []
            if proveedor_list.filter(estado_proveedor ='Inactivo').exists():
                for h in proveedor_list.filter(estado_proveedor ='Inactivo'):
                    proveedor_json.append({'id de proveedor':h.id,'Prov':h.nombre_proveedor,'RUT':h.rut_proveedor,'Correo':h.correo_proveedor,'Telefono':h.telefono_proveedor,'Direccion':h.direccion_proveedor,'Estado':h.estado_proveedor})
                    return Response({'Listado': proveedor_json})
            else:
                return Response({'Msj':'No se encuentran Proveedores Inactivos que concuerden'})    
        else:
            return Response({'Msj':'No existen Proveedores Inactivos que concuerden'})
    else:
        return Response({'Msj':'Error método no soportado'})

#renders
@login_required
def proveedores_main(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'p1/proveedores_main.html'
    return render(request,template_name,{'profile':profile})

@login_required
def proveedores_proveedores_add(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    data={ 'form': proveedorform()}
    template_name = 'p1/proveedores_add.html'
    return render(request,template_name,data,{'profile':profile})

@login_required
def proveedores_proveedor_save(request):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        rut = request.POST.get('rut')
        correo = request.POST.get('correo')
        telefono = request.POST.get('telefono')
        direccion = request.POST.get('direccion')
        validarRut(rut)
        existe = P1.objects.filter(rut_proveedor=rut).count()
        if validarRut(rut)==True:
            if existe >=1:
                messages.add_message(request, messages.INFO, 'Este rut ya se encuentra registrado')
                return redirect('proveedores_add')  
            else:
                proveedor_save = P1(
                nombre_proveedor = nombre,
                rut_proveedor = rut,
                correo_proveedor = correo,
                telefono_proveedor = telefono,
                direccion_proveedor = direccion
                )
                proveedor_save.save()
                proveedor_save.dato_producto.add()
                messages.add_message(request, messages.INFO, 'Prov ingresado con éxito')
                return redirect('proveedor_actlist_proveedores')
        else:
            messages.add_message(request, messages.INFO, 'Debes ingresar un rut valido')
            return redirect('proveedores_add')         
    else:
        messages.add_message(request, messages.INFO, 'Error en el método de envío')


@login_required
def proveedor_actlist_proveedores(request,page=None,search=None):
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
        h_count = P1.objects.filter(estado_proveedor='Activo').count()
        h_list_array = P1.objects.filter(estado_proveedor='Activo').order_by('estado_proveedor')
        for h in h_list_array:
            h_list.append({'id':h.id,'Proveedor':h.nombre_proveedor,'RUT':h.rut_proveedor,'Correo':h.correo_proveedor,'Telefono':h.telefono_proveedor,'Direccion':h.direccion_proveedor,'Estado':h.estado_proveedor})
    else:
        h_count = P1.objects.filter(estado_proveedor='Activo').filter(nombre_proveedor__icontains=search).count()
        h_list_array = P1.objects.filter(estado_proveedor='Activo').filter(nombre_proveedor__icontains=search).order_by('nombre_proveedor')
        for h in h_list_array:
            h_list.append({'id':h.id,'Proveedor':h.nombre_proveedor,'RUT':h.rut_proveedor,'Correo':h.correo_proveedor,'Telefono':h.telefono_proveedor,'Direccion':h.direccion_proveedor,'Estado':h.estado_proveedor})            
    paginator = Paginator(h_list, 5) 
    h_list_paginate= paginator.get_page(page)   
    template_name = 'p1/proveedores_proveedoract_list.html'
    return render(request,template_name,{'template_name':template_name,'h_list_paginate':h_list_paginate,'paginator':paginator,'page':page})

@login_required
def proveedoredit (request,id):
    profile = Profile.objects.get(user_id=request.user.id)
    if profile.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    proveedor= get_object_or_404(P1, id=id)
    data={'form' : proveedorform(instance=proveedor)}
    if request.method == 'POST':
        form = proveedorform(data=request.POST,instance=proveedor)
        rut = request.POST.get('rut_proveedor')
        validarRut(rut)
        existe = P1.objects.filter(rut_proveedor=rut).exclude(id=id).count()
        if validarRut(rut)==True:
            if existe >= 1:
                messages.add_message(request, messages.INFO, 'Este rut ya se encuentra registrado')
            else:
                if form.is_valid():
                    form.save() 
                    return redirect(to='proveedor_actlist_proveedores')
                else:
                    messages.add_message(request, messages.INFO, 'El formulario no es valido')
        else:
            messages.add_message(request, messages.INFO, 'El rut ingresado es invalido')
        data['form']=form
    return render(request,'p1/proveedores_ver.html',data,{'profile':profile})    

@login_required
def proveedor_inactlist_proveedores(request,page=None,search=None):
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
        h_count = P1.objects.filter(estado_proveedor='Inactivo').count()
        h_list_array = P1.objects.filter(estado_proveedor='Inactivo').order_by('estado_proveedor')
        for h in h_list_array:
            h_list.append({'id':h.id,'Proveedor':h.nombre_proveedor,'RUT':h.rut_proveedor,'Correo':h.correo_proveedor,'Telefono':h.telefono_proveedor,'Direccion':h.direccion_proveedor,'Estado':h.estado_proveedor})
    else:
        h_count = P1.objects.filter(estado_proveedor='Inactivo').filter(nombre_proveedor__icontains=search).count()
        h_list_array = P1.objects.filter(estado_proveedor='Inactivo').filter(nombre_proveedor__icontains=search).order_by('nombre_proveedor')
        for h in h_list_array:
            h_list.append({'id':h.id,'Proveedor':h.nombre_proveedor,'RUT':h.rut_proveedor,'Correo':h.correo_proveedor,'Telefono':h.telefono_proveedor,'Direccion':h.direccion_proveedor,'Estado':h.estado_proveedor})            
    paginator = Paginator(h_list, 5) 
    h_list_paginate= paginator.get_page(page)   
    template_name = 'p1/proveedores_proveedorinact_list.html'
    return render(request,template_name,{'template_name':template_name,'h_list_paginate':h_list_paginate,'paginator':paginator,'page':page})
