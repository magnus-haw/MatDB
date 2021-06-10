from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from .models import ITARMaterial, ITARMaterialVersion, ITARVariableProperty, ITARConstProperty, ITARMatrixProperty
from sources.models import Reference

from materials.views import mycolors
from materials.forms import UploadITARMaterialVersion
from software.file_formatters import PATO_formatter, FIAT_formatter, ICARUS_formatter
from software.models import ExportFormat, SoftwareVersion, Software, ITARExportFormat
from sources.models import Reference, Tutorial

import numpy as np
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import LinearAxis,Range1d
from bokeh.layouts import column

# Create your views here.

def itarmaterial_view(request, matpk):
    mat = get_object_or_404(ITARMaterial, pk=matpk)
    refs = Reference.objects.filter(itarmaterials = mat)
    print(refs)
    form_error = False
    form_success = False
    form_error_mesg = ""

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UploadITARMaterialVersion(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            try:
                # process the data in form.cleaned_data as required
                csvfile = request.FILES['file']
                pform = eval(form.cleaned_data["upload_format"].name + "_formatter()")
                pform.upload_file(csvfile, ITAR=True)
                print("finished upload")
                matv = ITARMaterialVersion.objects.get(material=form.cleaned_data["material"], version=form.cleaned_data["version"])
                pform.update_export_format(matv)
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
        form = UploadITARMaterialVersion(initial = {'material':mat.pk})

    context = {
            'material':mat,
            'references':refs,
            'form':form,
            'form_error':form_error,
            'error_mesg':form_error_mesg,
            'form_success':form_success,
            }
    return render(request, 'materials/material.html', context = context)

# def itarmaterial_version_view(request,matv_pk):
#     matv = get_object_or_404(ITARMaterialVersion, pk=matv_pk)
    constprops = matv.itarconstproperty_set.all()
    varprops = matv.itarvariableproperty_set.all().order_by('state')
    matrixprops = matv.itarmatrixproperty_set.all().order_by('state')
#     context = {
#             'matv':matv,
#             'constprops':constprops,
#             'varprops':varprops,
#             'matrixprops':matrixprops,

#             }
#     return render(request, 'materials/version.html', context = context)

def itarmaterial_version_view(request,matv_pk):
    matv = get_object_or_404(ITARMaterialVersion, pk=matv_pk)
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

    props = matv.itarmaterialpropertyinstance_set.all()

    constprops = ITARConstProperty.objects.filter(property_instance__in = props)
    varprops = ITARVariableProperty.objects.filter(property_instance__in = props)
    matrixprops = ITARMatrixProperty.objects.filter(property_instance__in = props)
    download = ITARExportFormat.objects.filter(material_version=matv)
    software = Software.objects.all()

    if request.method == 'POST' and 'views' in request.POST:
        soft_name = request.POST['views']
        print(soft_name)
        if soft_name == "All":
            constprops = matv.itarconstproperty_set.all().order_by('software')
            varprops = matv.itarvariableproperty_set.all().order_by('software', 'state')
            matrixprops = matv.itarmatrixproperty_set.all().order_by('software', 'state')
        else:
            software_i = Software.objects.get(name=soft_name)
            constprops = matv.itarconstproperty_set.all().filter(software=software_i)
            varprops = matv.itarvariableproperty_set.all().order_by('state').filter(software=software_i)
            matrixprops = matv.itarmatrixproperty_set.all().order_by('state').filter(software=software_i)

    context = {
            'matv':matv,
            'constprops':constprops,
            'varprops':varprops,
            'matrixprops':matrixprops,
            'download':download,
            'software':software,
            }
    return render(request, 'materials/version.html', context = context)

def itarvprop_view(request,vprop_pk):
    vprop = get_object_or_404(ITARVariableProperty, pk=vprop_pk)
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
