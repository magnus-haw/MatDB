from django.shortcuts import render, get_object_or_404, redirect
from .models import Software, SoftwareVersion
from sources.models import Reference, Tutorial

# Create your views here.
def index(request):
    softwares = Software.objects.all()
    last_modified = softwares.latest('last_modified').last_modified

    context = {
        'softwares':softwares,
        'last_modified':last_modified,
            }
    return render(request, 'software/index.html', context=context)

def software_view(request,swpk):
    sw = get_object_or_404(Software, pk=swpk)
    tuts = Tutorial.objects.filter(softwares = sw)
    refs = Reference.objects.filter(softwares = sw)

    context = {
            'software':sw,
            'tutorials':tuts,
            'refs':refs,
            }
    return render(request, 'software/software.html', context = context)

def software_version_view(request,swvpk):
    swv = get_object_or_404(SoftwareVersion, pk=swvpk)
    if swv.link:
        return redirect(swv.link)
    
    context = {
            'swv':swv,
            }
    return render(request, 'software/version.html', context = context)