from django.urls import path
from . import views

urlpatterns = [
    path('version/<int:matv_pk>',views.itarmaterial_version_view, name='itarversion-detail'),
    path('<int:matpk>',views.itarmaterial_view, name='itarmaterial-detail'),
    path('reference/<int:pk>',views.itarreference_view, name='itarreference-detail'),
]
