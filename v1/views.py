from contextlib import redirect_stderr
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
import sys
from itertools import cycle
from ordenescompra1.models import *
from p1.models import *
from v1.models import *
from productos.models import *
from v1.models import V1
from p1.models import P1
from django.db.models import Q
from django.views.generic import ListView,CreateView,DeleteView
from .forms import VendedorForm
from django.urls import reverse_lazy

# Create your views here.
class vendedoractlist(ListView):
    model=V1
    template_name='vendedoract_list.html'

    def get_queryset(self):
        return V1.objects.filter(estado_vendedor__startswith='Activo')

class vendedorinaclist(ListView):
    model=V1
    template_name='vendedorinac_list.html'

    def get_queryset(self):
        return V1.objects.filter(estado_vendedor__startswith='Inactivo')

class vendedoradd(CreateView):
    model=V1
    fields = '__all__'
    form_class: VendedorForm
    template_name='vendedor_add.html'
    success_url = reverse_lazy('vendedoract_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creacion vendedor'
        return context

class desactivarven(DeleteView):
    model=V1
    template_name='desactivar_ven.html'

    def post(self,request,pk,*args,**kwargs):
        object = V1.objects.get(id = pk)
        object.estado_vendedor = 'Inactivo'
        object.save()
        return redirect('vendedorinac_list')

class activarven(DeleteView):
    model=V1
    template_name='activar_ven.html'

    def post(self,request,pk,*args,**kwargs):
        object = V1.objects.get(id = pk)
        object.estado_vendedor = 'Activo'
        object.save()
        return redirect('vendedoract_list')

def vendedor_edit(request, id_vendedor):
    vendedor = V1.objects.get(id=id_vendedor)
    if request.method == 'GET':
        form = VendedorForm(instance=vendedor)
    else:
        form = VendedorForm (request.POST, instance=vendedor)
        if form.is_valid():
            form.save()
        return redirect('vendedoract_list')
    return render(request,'vendedor_add.html',{'form':form})




class inicio(ListView):
    model=V1
    template_name='inicio.html'

def validarRut(rut):
	rut = rut.upper();
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


#Guardar Vendores
@api_view(['POST'])
def vendedores_add_rest(request, format=None):
    if request.method == 'POST':
        nombre = request.data['nombre']
        rut = request.data['rut']
        telefono = request.data['telefono']
        correo = request.data['correo']
        idproveedor = request.data['id de proveedor']
        validarRut(rut)
        if validarRut(rut)==True:
            if V1.objects.filter(rut_vendedor=rut):
                return Response({'Msj':"Este rut ya se encuentra registrado"})
            else:
                if nombre == '' or rut == '' or telefono == '' or correo == '' :
                    return Response({'Msj': "Error, los datos no pueden estar en blanco"})
            vendedor_save = V1(
            nombre_vendedor = nombre,
            rut_vendedor = rut,
            telefono_vendedor = telefono,
            correo_vendedor = correo,
            dato_proveedor_id = idproveedor,
            )
            vendedor_save.save()
            return Response({'Msj':"Vendedor creado"})
        else:
            return Response({'Msj':"Ingrese rut valido"})        
    else:
        return Response ({'Msj': "Error, método no soportado"})


#Activar y Desactivar Vendes
@api_view(['POST'])
def vendedores_update_element_rest(request, format=None):
    if request.method == 'POST':
        vendedor_json = []
        vendedor_id = request.data['vendedor_id']
        estado = request.data['estado']
        if (estado != "Activo") and (estado != "Inactivo"):
            return Response ({'Msj':'formato de estado incorrecto, porfavor ingrese un estado valido, ej: Activo o Inactivo'})
        else:
            V1.objects.filter(pk=vendedor_id).update(estado_vendedor=estado)
        return Response({'Msj':'Estado modificado con éxito'})
    else:
        return Response({'Msj':"Error, método no soportado."})



#Listar Vendores Activos
@api_view(['GET'])
def vendedores_vendedoract_list_rest(request, format=None):
    if request.method == 'GET':
        vendedor_list = V1.objects.all().order_by('nombre_vendedor')
        vendedor_json = []
        if vendedor_list.filter(estado_vendedor ='Activo').exists():
            for h in vendedor_list.filter(estado_vendedor ='Activo'):
                vendedor_json.append({'id de vendedor':h.id,'Vendedor':h.nombre_vendedor,'RUT':h.rut_vendedor,'Telefono':h.telefono_vendedor,'Correo':h.correo_vendedor,'Estado':h.estado_vendedor})
            return Response({'Listado':vendedor_json})
        else:
                return Response({'Msj':'No se encuentran vendedores Activos'}) 
    else:
        return Response({'Msj':"Error: Método no soportado"})


#Listar Vendedores Inactivos
@api_view(['GET'])
def vendedores_vendedorinac_list_rest(request, format=None):
    if request.method == 'GET':
        vendedor_list = V1.objects.all().order_by('nombre_vendedor')
        vendedor_json = []
        if vendedor_list.filter(estado_vendedor ='Inactivo').exists():
            for h in vendedor_list.filter(estado_vendedor ='Inactivo'):
                vendedor_json.append({'id de vendedor':h.id,'Vendedor':h.nombre_vendedor,'RUT':h.rut_vendedor,'Telefono':h.telefono_vendedor,'Correo':h.correo_vendedor,'Estado':h.estado_vendedor})
            return Response({'Listado':vendedor_json})
        else:
                return Response({'Msj':'No se encuentran vendedores Inactivos'}) 
    else:
        return Response({'Msj':"Error: Método no soportado"})


#Buscar Vendes Activos
@api_view(['POST'])
def vendedores_vendedoract_list_contains(request, format=None):
    if request.method == 'POST':
        vendedor_list = V1.objects.all().order_by('nombre_vendedor')
        search = request.data['search']
        vendedor_list_count = V1.objects.filter(Q(nombre_vendedor__icontains=search)|Q(rut_vendedor__icontains=search)).count()
        if vendedor_list_count > 0:
            vendedor_list = V1.objects.filter(Q(nombre_vendedor__icontains=search)|Q(rut_vendedor__icontains=search))
            vendedor_json = []
            if vendedor_list.filter(estado_vendedor ='Activo').exists():
                for h in vendedor_list.filter(estado_vendedor ='Activo'):
                    vendedor_json.append({'id de vendedor':h.id,'Vendedor':h.nombre_vendedor,'RUT':h.rut_vendedor,'Telefono':h.telefono_vendedor,'Correo':h.correo_vendedor,'Estado':h.estado_vendedor})
                    return Response({'Listado': vendedor_json})
            else:
                return Response({'Msj':'No se encuentran vendedores activos que concuerden'})    
        else:
            return Response({'Msj':'No existen vendedores Activos que concuerden'})
    else:
        return Response({'Msj':'Error método no soportado'}) 


#Buscar Vendes Inactivos
@api_view(['POST'])
def vendedores_vendedorinac_list_contains(request, format=None):
    if request.method == 'POST':
        vendedor_list = V1.objects.all().order_by('nombre_vendedor')
        search = request.data['search']
        vendedor_list_count = V1.objects.filter(Q(nombre_vendedor__icontains=search)|Q(rut_vendedor__icontains=search)).count()
        if vendedor_list_count > 0:
            vendedor_list = V1.objects.filter(Q(nombre_vendedor__icontains=search)|Q(rut_vendedor__icontains=search))
            vendedor_json = []
            if vendedor_list.filter(estado_vendedor ='Inactivo').exists():
                for h in vendedor_list.filter(estado_vendedor ='Inactivo'):
                    vendedor_json.append({'id de vendedor':h.id,'Vendedor':h.nombre_vendedor,'RUT':h.rut_vendedor,'Telefono':h.telefono_vendedor,'Correo':h.correo_vendedor,'Estado':h.estado_vendedor})
                    return Response({'Listado': vendedor_json})
            else:
                return Response({'Msj':'No se encuentran vendedores Inactivos que concuerden'})    
        else:
            return Response({'Msj':'No existen vendedores Inactivos que concuerden'})
    else:
        return Response({'Msj':'Error método no soportado'})
        