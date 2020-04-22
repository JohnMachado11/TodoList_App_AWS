from django.urls import path     
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('create', views.create),
    path('login', views.login),
    path('reset', views.reset),
    path('tasks', views.appointment),
    path('update/table', views.table_update),
    path('tasks/add', views.addroute),
    path('addroute', views.adding),
    path('tasks/<int:id>', views.edit_route),
    path('update/<int:id>', views.update),
    path('<int:id>/destroy', views.delete),
]