from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.conf import settings
from django.views.static import serve
from store import views

admin.site.site_header = "Mushora Farms Management"
admin.site.site_title = "Mushora Farms Admin"
admin.site.index_title = "Manage products, stock, prices and orders"

urlpatterns = [
    path("manage/", admin.site.urls),
    path("accounts/login/", auth_views.LoginView.as_view(template_name="store/login.html"), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("accounts/register/", views.register, name="register"),
    path("my-orders/", views.my_orders, name="my_orders"),
    path("", views.home, name="home"),
    path("order/", views.place_order, name="place_order"),
    path("order/confirmation/<int:order_id>/", views.order_confirmation, name="order_confirmation"),
    path("media/<path:path>", serve, {"document_root": settings.MEDIA_ROOT}),
]
