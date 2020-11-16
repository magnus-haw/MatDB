from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.views import generic
from django.contrib import messages
from django.urls import reverse
from django.db import transaction

from .models import Material, MaterialVersion, VariableProperties, ConstProperty, MatrixProperty

# Write your views here

def index(request):
    nmat = Material.objects.count()
    mats = Material.objects.all()
    context = {
        'materials':mats,
        'nmaterials':nmat,
            }
    return render(request, 'materials/index.html', context=context)

def material_view(request,matpk):
    matv = get_object_or_404(MaterialVersion, pk=matpk)
    constprops = matv.constproperty_set.all()
    varprops = matv.variableproperties_set.all().order_by('state')
    
    context = {
            'matv':matv,
            'constprops':constprops,
            'varprops':varprops,
            'rows':rows,
            }
    return render(request, 'materials/version.html', context = context)


def material_version_view(request,matv_pk):
    matv = get_object_or_404(MaterialVersion, pk=matv_pk)
    constprops = matv.constproperty_set.all()
    varprops = matv.variableproperties_set.all().order_by('state')
    
    context = {
            'matv':matv,
            'constprops':constprops,
            'varprops':varprops,
            }
    return render(request, 'materials/version.html', context = context)



