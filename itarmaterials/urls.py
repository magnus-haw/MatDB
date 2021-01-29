from django.urls import path
from . import views

urlpatterns = [
    path('version/<int:matv_pk>',views.itarmaterial_version_view, name='itarversion-detail'),
    path('<int:matpk>',views.itarmaterial_view, name='itarmaterial-detail'),
    path('variable_property/<int:vprop_pk>',views.itarvprop_view, name='itarvprop-detail'),
]
