from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('version/<int:swvpk>',views.software_version_view, name='sw-version-detail'),
    path('<int:swpk>',views.software_view, name='sw-detail'),
]
