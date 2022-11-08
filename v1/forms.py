from dataclasses import field
from django.forms import ModelForm
from .models import *

class VendedorForm(ModelForm):
    class Meta:
        model = V1
        fields = '__all__'