from django import forms
from .models import Material
from software.models import Software

class UploadMaterialVersion(forms.Form):
    material = forms.ModelChoiceField(queryset=Material.objects.all())
    version = forms.CharField(max_length=50)
    file = forms.FileField()
    upload_format = forms.ModelChoiceField(queryset=Software.objects.all())
    