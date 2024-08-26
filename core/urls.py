from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('user/register/', views.register),
    path('user/login/', views.Login),
    path('activate/<str:uidb64>/<str:token>/', views.activate_Email, name='activate'),
    path('user/child_register/', views.child_register),
    path('user/update/parent/', views.update_parent),
    path('user/update/child/', views.update_child),
    path('user/get/get_all_children/', views.get_all_children),
    path('user/get/parent/', views.get_parent),
    path('user/get/child/', views.get_child),
    path('nova/', views.nova, name='nova'),

    
]