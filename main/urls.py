import imp
from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('group/<str:name>/<str:code>/', views.group , name='group'),
    
    path('spec/<int:id>', views.spec, name='spec'),
    path('signup', views.signup, name = 'signup'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('my_subjects', views.my_subjects, name='my_subjects'),
    path('result/<str:code>', views.result, name='result'),

]
