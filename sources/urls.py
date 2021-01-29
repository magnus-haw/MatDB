from django.urls import path
from . import views

urlpatterns = [
    path('tutorials/<int:pk>',views.tutorial_view, name='tutorial-detail'),
]
