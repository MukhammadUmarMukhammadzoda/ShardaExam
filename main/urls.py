import imp
from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('group/<str:name>/<str:code>/', views.group , name='group'),
    
    path('spec/<int:id>', views.spec, name='spec'),
    
    path('api/', views.API.as_view(), name='api'),
]
