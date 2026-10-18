from django.conf import settings
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=120)
    weight = models.CharField(max_length=30)
    price = models.PositiveIntegerField()
    description = models.CharField(max_length=220, blank=True)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.weight})"

class Order(models.Model):
    PAYMENT_CHOICES = [
        ("cod", "Cash on delivery"),
        ("upi", "UPI (confirm details on WhatsApp)"),
    ]
    STATUS_CHOICES = [
        ("new", "New"),
        ("confirmed", "Confirmed"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                             null=True, blank=True, related_name="mushroom_orders")
    customer_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    area = models.CharField(max_length=120, blank=True)
    preferred_date = models.DateField(null=True, blank=True)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default="cod")
    notes = models.TextField(blank=True)
    items_json = models.JSONField(default=list)
    total = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.pk} — {self.customer_name}"

class SiteSettings(models.Model):
    business_name = models.CharField(max_length=120, default="Mushora Farms")
    contact_phone = models.CharField(max_length=20, default="9550957029",
                                     help_text="Public customer contact number.")
    whatsapp_number = models.CharField(max_length=20, default="919550957029",
                                       help_text="WhatsApp number with country code, digits only (e.g. 919550957029).")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Website settings"
        verbose_name_plural = "Website settings"

    def __str__(self):
        return self.business_name

    @classmethod
    def current(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
