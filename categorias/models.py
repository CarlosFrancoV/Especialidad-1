from tabnanny import verbose
from django.db import models

# Create your models here.
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