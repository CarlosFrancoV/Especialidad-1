from django.db import models
from p1.models import * 
from productos.models import *
from v1.models import *
from .choice import estado



# Create your models here.
class Ordencompra1(models.Model):
    proveedor = models.ForeignKey(P1, on_delete=models.CASCADE)
    vendedor = models.ForeignKey(V1, on_delete=models.CASCADE)
    numero_pedido = models.IntegerField(null=True,blank=True,verbose_name='Numero Pedido')
    precio_orden = models.IntegerField(null=True,blank=True,verbose_name='Precio Orden')
    cantidad_orden = models.IntegerField(null=True,blank=True,verbose_name='Cantidad Orden')
    created = models.DateTimeField(auto_now_add=True)
    estado_pedido = models.CharField(max_length=100, null=True,blank=True,choices=estado,default='Pendiente',verbose_name='Estado Pedido')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE,null=True,blank=True)

    class Meta:
        verbose_name = 'Ordencompra1'
        verbose_name_plural = 'Ordenescompra1'
        ordering =['numero_pedido']
    def __str__(self):
        return self.numero_pedido


class Detalle1(models.Model):
    dato_compra = models.ForeignKey(Ordencompra1, on_delete=models.CASCADE)
    dato_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)


class Meta:
    verbose_name = 'Detalle1'
    verbose_name_plural = 'Detalles1'
    ordering =['numero_pedido']
def __str__(self):
    return self.numero_pedido