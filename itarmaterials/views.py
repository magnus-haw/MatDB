from django.shortcuts import render, get_object_or_404
from .models import ITARMaterial, ITARMaterialVersion, ITARVariableProperty
from sources.models import Reference

from materials.views import mycolors

import numpy as np
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import LinearAxis,Range1d
from bokeh.layouts import column

# Create your views here.
def itarmaterial_view(request,matpk):
    mat = get_object_or_404(ITARMaterial, pk=matpk)
    refs = Reference.objects.filter(itarmaterials = mat)

    context = {
            'material':mat,
            'references':refs,
            }
    return render(request, 'materials/material.html', context = context)

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
