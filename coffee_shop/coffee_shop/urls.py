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
from orders import views as order_views
from django.conf import settings
from django.conf.urls.static import static
from menu.views import MenuListView
from orders.views import (
    ApplyDiscountView,
    AddToCartView,
    RemoveFromCartView,
    ViewCartView,
    PlaceOrderView,
    OrderHistoryView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", MenuListView.as_view()),

    path("register/", views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="auth/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("menu/", MenuListView.as_view(), name="menu-list"),

    path("cart/", ViewCartView.as_view(), name="view-cart"),
    path("cart/add/<int:item_id>/", AddToCartView.as_view(), name="add-to-cart"),
    path("cart/remove/<int:item_id>/", RemoveFromCartView.as_view(), name="remove-from-cart"),
    path("cart/apply-discount/<int:discount_id>/", ApplyDiscountView.as_view(), name="apply-discount"),
    path("order/place/", PlaceOrderView.as_view(), name="place-order"),
    path("orders/history/", OrderHistoryView.as_view(), name="order-history"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)