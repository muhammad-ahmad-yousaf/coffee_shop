"""
URL configuration for coffee_shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from menu.views import menu_list
from orders import views as order_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path("register/", views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="auth/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("welcome/", views.welcome_view, name="welcome"),

    path("menu/", menu_list, name="menu-list"),

    path("cart/", order_views.view_cart, name="view-cart"),
    path("cart/add/<int:item_id>/", order_views.add_to_cart, name="add-to-cart"),
    path("cart/remove/<int:item_id>/", order_views.remove_from_cart, name="remove-from-cart"),
    path("order/place/", order_views.place_order, name="place-order"),
    path("orders/history/", order_views.order_history, name="order-history"),
]
