from django.urls import path
from . import views

urlpatterns = [
    path("connect/", views.connect_clover, name="connect_clover"),
    path("callback/", views.clover_callback, name="clover_callback"),

]
