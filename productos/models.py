from tabnanny import verbose
from django.db import models

# Create your models here.
class Producto(models.Model):
    nombre_producto = models.CharField(max_length=100,blank=True, verbose_name='Nombre Producto')
    sku_producto = models.CharField(max_length=12,blank=True, verbose_name='SKU Producto')
    codigo_barras_producto = models.CharField(max_length=12,blank=True, verbose_name='Codigo Barras Producto')
    precio_producto = models.CharField(max_length=9,blank=True, verbose_name='Precio Producto')
    costo_producto = models.CharField(max_length=9,blank=True, verbose_name='Precio Producto')
    stock_producto = models.IntegerField(null=True,blank=True,verbose_name='Stock Producto')
    stock_promedio = models.IntegerField(null=True,blank=True,verbose_name='Stock Promedio Producto')
    created = models.DateTimeField(auto_now_add=True)
    state = models.CharField(max_length=50,null=True,blank=True,default='Activo',verbose_name='Estado Prodcuto')

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering =['nombre_producto']
    def __str__(self):
        return self.nombre_producto

#Categorias
class Categoria(models.Model):
    nombre_categoria = models.CharField(max_length=50,null=True,blank=True,verbose_name='Nombre Categoria')
    state = models.CharField(max_length=50,null=True,blank=True,default='Activo',verbose_name='Estado Categoria')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name='Categoria'
        verbose_name_plural ='Categorias'
        ordering = ['nombre_categoria']

    def __str__(self):
        return self.nombre_categoria
