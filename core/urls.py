from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('user/register/', views.register),
    path('user/login/', views.Login),
    path('activate/<str:uidb64>/<str:token>/', views.activate_Email, name='activate'),
    path('user/child_register/', views.child_register),
    path('user/update/parent/', views.update_parent),
    
]