import os
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.views import generic
from django.contrib import messages
from django.urls import reverse
from django.db import transaction

from .models import Material, MaterialVersion, VariableProperty 
from .models import ConstProperty, MatrixProperty, Reference
from .export.codes import *
from .forms import UploadMaterialVersion

from itarmaterials.models import ITARMaterial
from software.file_formatters import PATO_formatter, FIAT_formatter, ICARUS_formatter
from software.models import ExportFormat, SoftwareVersion

import numpy as np
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import LinearAxis,Range1d
from bokeh.layouts import column
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
    form_error = False
    form_success = False

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UploadMaterialVersion(request.POST, request.FILES)
        # check whether it's valid:
        print(request.FILES)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            csvfile = request.FILES['file']
            pform = PATO_formatter()
            pform.upload_file(csvfile)
            # redirect to a new URL:
            form_success = True
        else:
            print(form.errors)
            form_error = True
    # if a GET (or any other method) we'll create a blank form
    else:
        form = UploadMaterialVersion(initial = {'material':mat.pk})

    context = {
            'material':mat,
            'references':refs,
            'form':form,
            'form_error':form_error,
            'form_success':form_success,
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
    if request.method == 'POST' and 'export_codes' in request.POST:
        softv_pk = request.POST['export_codes']
        softv = get_object_or_404(SoftwareVersion, pk=softv_pk)
        eval_name = softv.software.name + "_formatter()"
        class_export_model = eval(eval_name)
        file_path = class_export_model.export_file(matv,softv)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(),content_type='application/force-download')
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                os.remove(file_path)
                return response
        # raise Http404
        return HttpResponseRedirect(request.path_info)
    
    constprops = matv.constproperty_set.all()
    varprops = matv.variableproperty_set.all().order_by('state')
    matrixprops = matv.matrixproperty_set.all().order_by('state')
    download = ExportFormat.objects.filter(material_version=matv)
    context = {
            'matv':matv,
            'constprops':constprops,
            'varprops':varprops,
            'matrixprops':matrixprops,
            'download':download,
            }
    return render(request, 'materials/version.html', context = context)

mycolors = ['green','red','blue','cyan','orange','black','magenta','purple','olive','lime','yellow','gold','darkred','salmon',
            'deeppink','coral','turquoise','teal','darkkhaki','khaki','navy','steelblue']

def vprop_view(request,vprop_pk):
    vprop = get_object_or_404(VariableProperty, pk=vprop_pk)
    plist = np.unique(vprop.p)
    items = zip(vprop.p,vprop.T,vprop.values)

    ### Plotting section
    fig = figure(x_axis_label="Temp (K)", y_axis_label=vprop.name + " ["+vprop.unit.symbol+"]",plot_width =650,plot_height =300,sizing_mode='scale_width')
    for i in range(0,len(plist)):
        p = plist[i]
        T = vprop.T[vprop.p == p]
        vals = vprop.values[vprop.p == p]
        fig.line(T,vals, legend_label= str(p),line_width = 2, line_color=mycolors[i])
    fig.legend.click_policy="hide"
    #Store components
    script, div = components(fig)
    return render(request, 'materials/vprop_detail.html', {'vprop':vprop,'script':script,'div':div,'items':items})

