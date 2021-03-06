from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('version/<int:matv_pk>',views.material_version_view, name='version-detail'),
    path('variable_property/<int:vprop_pk>',views.vprop_view, name='vprop-detail'),
    path('<int:matpk>',views.material_view, name='material-detail'),
    path('reference/<int:pk>',views.reference_view, name='reference-detail'),
]
