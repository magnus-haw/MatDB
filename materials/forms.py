from django import forms
from django.core.validators import int_list_validator

from .models import Material
from itarmaterials.models import ITARMaterial
from software.models import Software

class UploadMaterialVersion(forms.Form):
    material = forms.ModelChoiceField(queryset=Material.objects.all())
    version = forms.CharField(max_length=50, validators=[int_list_validator(sep='.')])
    file = forms.FileField()
    upload_format = forms.ModelChoiceField(queryset=Software.objects.all())
    
class UploadITARMaterialVersion(forms.Form):
    material = forms.ModelChoiceField(queryset=ITARMaterial.objects.all())
    version = forms.CharField(max_length=50, validators=[int_list_validator(sep='.')])
    file = forms.FileField()
    upload_format = forms.ModelChoiceField(queryset=Software.objects.all())
    