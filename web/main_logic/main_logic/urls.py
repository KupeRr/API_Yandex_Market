from django.contrib import admin
from django.urls import path

#TODO re_path is rly strong instrument, need more info about it
from django.urls import re_path

from main_window import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),

    re_path(r'^products/$', views.products),
    re_path(r'^users/$', views.users),
    re_path(r'^products/(?P<productid>\d+)/', views.products),
    re_path(r'^users/(?P<id>\d+)/(?P<name>\D+)/', views.users),

    #TODO What's better?
    #path('products/', views.products),
    #path('users/', views.users),
    #path('products/<int:productid>/', views.products),
    #path('users/<int:id>/<name>/', views.users),
]
