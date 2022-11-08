from rest_framework import serializers
from .models import *

class Ordencompra1Serializer(serializers.ModelSerializer):
    class Meta:
        model = Ordencompra1
        fields = '__all__'

class Ordencompra1SerializerEdit(serializers.ModelSerializer):
    class Meta:
        model = Ordencompra1
        fields = ('cantidad_orden','precio_orden')

class Ordencompra1SerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = Ordencompra1
        fields = ('cantidad_orden','precio_orden','proveedor','vendedor','numero_pedido','producto')

class Ordencompra1SerializerChangeState(serializers.ModelSerializer):
    class Meta:
        model = Ordencompra1
        fields = ('estado_pedido',)

class ProductsDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'