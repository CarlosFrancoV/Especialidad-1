from django import forms 
from p1.models import *
from productos.models import * 

class CustomMMCF(forms.ModelMultipleChoiceField):
    def label_from_instance(self, Producto):
        return "%s" % Producto.nombre_producto

class proveedorform(forms.ModelForm):
    dato_producto = CustomMMCF(queryset=Producto.objects.all(),widget=forms.SelectMultiple(attrs={'class':'form-select','aria-label':'size 3 select example'}))
    correo_proveedor = forms.EmailField(max_length = 30,widget=forms.EmailInput(attrs={'class':'form-control','type':'text','size':'30','placeholder':'Ej: proveedor@mail.com','pattern':'[^@\s]+@[^@\s]+.com'}))
    class Meta:
        model = P1
        fields = ['nombre_proveedor','rut_proveedor' ,'correo_proveedor','telefono_proveedor','direccion_proveedor','estado_proveedor','dato_producto']
        widgets ={
            'nombre_proveedor' : forms.TextInput(attrs={'class':'form-control','type':'text'}),
            'rut_proveedor' : forms.NumberInput(attrs={'class':'form-control','type':'text','pattern':'\d{3,8}-[\d|kK]{1}','title':'Debe ser un Rut válido'}),
            'correo_proveedor' : forms.EmailInput(attrs={'class':'form-control','type':'text','size':'30'}),
            'telefono_proveedor' : forms.TextInput(attrs={'class':'form-control','type':'tel','pattern':'[0-9]{9}','placeholder':'Ej:912345678'}),
            'direccion_proveedor' : forms.TextInput(attrs={'class':'form-control','type':'text'}),
            'estado_proveedor' : forms.RadioSelect()
        }