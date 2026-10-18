from django.contrib import admin
from .models import Product, Order, SiteSettings

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "weight", "price", "available")
    list_editable = ("price", "available")
    list_filter = ("available",)
    search_fields = ("name", "weight")
    fields = ("name", "weight", "price", "description", "image", "available")

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer_name", "phone", "total", "payment_method", "status", "created_at")
    list_filter = ("status", "payment_method", "created_at")
    list_editable = ("status",)
    search_fields = ("customer_name", "phone", "address", "user__username")
    readonly_fields = ("created_at",)
    list_select_related = ("user",)

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("business_name", "contact_phone", "whatsapp_number", "updated_at")
    fields = ("business_name", "contact_phone", "whatsapp_number")
    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()
    def has_delete_permission(self, request, obj=None):
        return False
