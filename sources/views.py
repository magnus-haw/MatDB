from django.shortcuts import render, get_object_or_404, redirect
from .models import Reference, Tutorial

# Create your views here.

def tutorial_view(request,pk):
    tut = get_object_or_404(Tutorial, pk=pk)
    if tut.link:
        return redirect(tut.link)

    context = {
            'tutorial':tut,
            }
    return render(request, 'sources/tutorial.html', context = context)