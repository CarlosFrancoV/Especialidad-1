from django.db import models
from p1.models import *



# Create your models here.
class V1(models.Model):
    dato_proveedor = models.ForeignKey(P1, on_delete=models.CASCADE)
    nombre_vendedor = models.CharField(max_length=100,blank=True, verbose_name='Nombre Vendedor')
    rut_vendedor = models.CharField(max_length=13,blank=True,verbose_name='Rut Vendedor')
    telefono_vendedor = models.CharField(max_length=15,blank=True,verbose_name='Telefono Vendedor')
    correo_vendedor = models.CharField(max_length=50, blank=True,verbose_name='Correo Vendedor')
    estado_vendedor = models.CharField(max_length=20, blank=True,null=True,default='Activo', verbose_name='Estado Vendedor')
    
    class Meta:
        verbose_name = 'V1'
        verbose_name_plural = 'Vends'
        ordering =['nombre_vendedor']
    def __str__(self):
        return self.nombre_vendedor

