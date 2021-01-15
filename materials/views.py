from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.views import generic
from django.contrib import messages
from django.urls import reverse
from django.db import transaction

from .models import Material, MaterialVersion, VariableProperty 
from .models import ConstProperty, MatrixProperty, Reference
from itarmaterials.models import ITARMaterial

# Write your views here

def index(request):
    nmat = Material.objects.count()
    mats = Material.objects.all()
    itars = ITARMaterial.objects.all()
    last_modified = mats.latest('last_modified').last_modified

    context = {
        'materials':mats,
        'itars':itars,
        'nmaterials':nmat,
        'last_modified':last_modified,
            }
    return render(request, 'materials/index.html', context=context)

def material_view(request,matpk):
    mat = get_object_or_404(Material, pk=matpk)
    refs = Reference.objects.filter(material_version__material = mat)

    context = {
            'material':mat,
            'references':refs,
            }
    return render(request, 'materials/material.html', context = context)

def reference_view(request,pk):
    ref = get_object_or_404(Reference, pk=pk)

    context = {
            'reference':ref,
            }
    return render(request, 'materials/reference.html', context = context)

def material_version_view(request,matv_pk):
    matv = get_object_or_404(MaterialVersion, pk=matv_pk)
    constprops = matv.constproperty_set.all()
    varprops = matv.variableproperty_set.all().order_by('state')
    matrixprops = matv.matrixproperty_set.all().order_by('state')
    context = {
            'matv':matv,
            'constprops':constprops,
            'varprops':varprops,
            'matrixprops':matrixprops,

            }
    return render(request, 'materials/version.html', context = context)



