from django.shortcuts import render, get_object_or_404
from .models import ITARMaterial, ITARMaterialVersion, ITARReference

# Create your views here.
def itarmaterial_view(request,matpk):
    mat = get_object_or_404(ITARMaterial, pk=matpk)
    refs = ITARReference.objects.filter(material_version__material = mat)

    context = {
            'material':mat,
            'references':refs,
            }
    return render(request, 'materials/material.html', context = context)

def itarreference_view(request,pk):
    ref = get_object_or_404(ITARReference, pk=pk)

    context = {
            'reference':ref,
            }
    return render(request, 'materials/reference.html', context = context)

def itarmaterial_version_view(request,matv_pk):
    matv = get_object_or_404(ITARMaterialVersion, pk=matv_pk)
    constprops = matv.itarconstproperty_set.all()
    varprops = matv.itarvariableproperty_set.all().order_by('state')
    matrixprops = matv.itarmatrixproperty_set.all().order_by('state')
    context = {
            'matv':matv,
            'constprops':constprops,
            'varprops':varprops,
            'matrixprops':matrixprops,

            }
    return render(request, 'materials/version.html', context = context)