import os
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.views import generic
from django.contrib import messages
from django.urls import reverse
from django.db import transaction
from django.db.utils import DEFAULT_DB_ALIAS
from django.contrib.admin.utils import NestedObjects
from django.core import serializers

from .models import Material, MaterialVersion, VariableProperty 
from .models import ConstProperty, MatrixProperty
from .forms import UploadMaterialVersion

from itarmaterials.models import ITARMaterial
from software.file_formatters import PATO_formatter, FIAT_formatter, ICARUS_formatter
from software.models import SoftwareVersion, Software
from sources.models import Reference, Tutorial

import numpy as np
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import LinearAxis,Range1d
from bokeh.layouts import column
# Write your views here

def export_to_json(query):
    collector = NestedObjects(using=DEFAULT_DB_ALIAS)
    collector.collect(query)
    related_objects = collector.data
    related_objects = [instance for cls, instances in collector.data.items() for instance in instances]
    data = serializers.serialize("json", related_objects)
    return data

def index(request):
    nmat = Material.objects.count()
    mats = Material.objects.all()
    itars = ITARMaterial.objects.all()
    try:
        last_modified = mats.latest('last_modified').last_modified
    except:
        last_modified = None

    context = {
        'materials':mats,
        'itars':itars,
        'nmaterials':nmat,
        'last_modified':last_modified,
            }
    return render(request, 'materials/index.html', context=context)

def material_view(request,matpk):
    mat = get_object_or_404(Material, pk=matpk)
    refs = Reference.objects.filter(materials = mat)

    form_error = False
    form_success = False
    form_error_mesg = ""

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UploadMaterialVersion(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            try:
                # process the data in form.cleaned_data as required
                csvfile = request.FILES['file']
                pform = eval(form.cleaned_data["upload_format"].name + "_formatter()")
                pform.upload_file(csvfile)
                print("finished upload")
                matv = MaterialVersion.objects.get(material=form.cleaned_data["material"], version=form.cleaned_data["version"])

                # redirect to a new URL:
                form_success = True
            except Exception as inst:
                print(inst)
                form_error = True
                form_error_mesg = inst
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
            'error_mesg':form_error_mesg,
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

    props = matv.materialpropertyinstance_set.all()
    software = Software.objects.all()
    software_versions = SoftwareVersion.objects.filter(can_export=True)
    
    constprops = ConstProperty.objects.filter(property_instance__in = props)
    varprops = VariableProperty.objects.filter(property_instance__in = props)
    matrixprops = MatrixProperty.objects.filter(property_instance__in = props)

    if request.method == 'POST' and 'views' in request.POST:
        soft_name = request.POST['views']
        print(soft_name)
        if soft_name == "All":
            constprops = ConstProperty.objects.filter(property_instance__in = props).order_by('property_instance__state')
            varprops = VariableProperty.objects.filter(property_instance__in = props).order_by('property_instance__state')
            matrixprops = MatrixProperty.objects.filter(property_instance__in = props).order_by('property_instance__state')
        else:
            softv = Software.objects.get(name=soft_name).get_latest_version()
            varprops = VariableProperty.objects.filter(property_instance__property__in=softv.material_properties.all()) & VariableProperty.objects.filter(property_instance__material_version=matv)
            constprops = ConstProperty.objects.filter(property_instance__property__in=softv.material_properties.all()) & ConstProperty.objects.filter(property_instance__material_version=matv)
            matrixprops = MatrixProperty.objects.filter(property_instance__property__in=softv.material_properties.all()) & MatrixProperty.objects.filter(property_instance__material_version=matv)

    context = {
            'matv':matv,
            'constprops':constprops,
            'varprops':varprops,
            'matrixprops':matrixprops,
            'software_versions':software_versions,
            'software':software,
            }
    return render(request, 'materials/version.html', context = context)

mycolors = ['green','red','blue','cyan','orange','black','magenta','purple','olive','lime','yellow','gold','darkred','salmon',
            'deeppink','coral','turquoise','teal','darkkhaki','khaki','navy','steelblue']

###
# def export_material_version(request, matv_pk, fileformat):
#     matv = get_object_or_404(MaterialVersion, pk=matv_pk)
#     class_export_model = get_formatter(fileformat)
#     file_path = class_export_model.export_file(matv)
#     if os.path.exists(file_path):
#         with open(file_path, 'rb') as fh:
#             response = HttpResponse(fh.read(),content_type='application/force-download')
#             response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
#             os.remove(file_path)
#             return response
#     return HttpResponseRedirect(request.path_info)


def vprop_view(request,vprop_pk):
    vprop = get_object_or_404(VariableProperty, pk=vprop_pk)
    plist = np.unique(vprop.p)
    items = zip(vprop.p,vprop.T,vprop.values)

    ### Plotting section
    fig = figure(x_axis_label="Temp (K)", y_axis_label=vprop.property_instance.property.name + " ["+vprop.property_instance.property.unit.symbol+"]",plot_width =650,plot_height =300,sizing_mode='scale_width')
    for i in range(0,len(plist)):
        p = plist[i]
        T = vprop.T[vprop.p == p]
        vals = vprop.values[vprop.p == p]
        fig.line(T,vals, legend_label= str(p),line_width = 2, line_color=mycolors[i])
    fig.legend.click_policy="hide"
    #Store components
    script, div = components(fig)
    return render(request, 'materials/vprop_detail.html', {'vprop':vprop,'script':script,'div':div,'items':items})

