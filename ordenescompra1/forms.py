from dataclasses import field
from pydoc import text
from tkinter import Widget
from turtle import textinput
from typing import Text
from django.forms import ModelForm, TextInput, Textarea
from .models import *

class Ordencompra1Form(ModelForm):
    class Meta:
        model = Ordencompra1
        fields = ('cantidad_orden','precio_orden')
        

class ProductsForm(ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'


