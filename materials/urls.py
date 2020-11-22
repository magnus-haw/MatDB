from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('version/<int:matv_pk>',views.material_version_view, name='version-detail'),
]
