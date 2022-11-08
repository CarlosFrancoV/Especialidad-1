from django.db import models
from productos.models import * 
from .choice import estado
# Create your models here.

class P1(models.Model):
    dato_producto = models.ManyToManyField(Producto,verbose_name='Productos',related_name="get_productos")
    nombre_proveedor = models.CharField(max_length=100,blank=True, verbose_name='Nombre Proveedor')
    rut_proveedor = models.CharField(max_length=13,blank=True,verbose_name='Rut Proveedor')
    correo_proveedor = models.CharField(max_length=50, blank=True,verbose_name='Correo Proveedor')
    telefono_proveedor = models.CharField(max_length=15,blank=True,verbose_name='Telefono Proveedor')
    direccion_proveedor = models.CharField(max_length=60,blank=True,null=True,verbose_name='Direccion Proveedor')
    estado_proveedor = models.CharField(max_length=100, null=True,blank=False,choices=estado,default='Activo',verbose_name='Estado Proveedor')

    class Meta:
        verbose_name = 'P1'
        verbose_name_plural = 'P1'
        ordering =['nombre_proveedor']
    def __str__(self):
        return self.nombre_proveedor

