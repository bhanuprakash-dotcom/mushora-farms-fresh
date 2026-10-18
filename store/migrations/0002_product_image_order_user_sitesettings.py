from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
        ("store", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]
    operations = [
        migrations.AddField(
            model_name="product",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="products/"),
        ),
        migrations.AddField(
            model_name="order",
            name="user",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                    related_name="mushroom_orders", to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name="SiteSettings",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("business_name", models.CharField(default="Mushora Farms", max_length=120)),
                ("contact_phone", models.CharField(default="9550957029", help_text="Public customer contact number.", max_length=20)),
                ("whatsapp_number", models.CharField(default="919550957029", help_text="WhatsApp number with country code, digits only (e.g. 919550957029).", max_length=20)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"verbose_name": "Website settings", "verbose_name_plural": "Website settings"},
        ),
    ]
