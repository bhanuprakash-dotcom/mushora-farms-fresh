from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="Product",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("weight", models.CharField(max_length=30)),
                ("price", models.PositiveIntegerField()),
                ("description", models.CharField(blank=True, max_length=220)),
                ("available", models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("customer_name", models.CharField(max_length=120)),
                ("phone", models.CharField(max_length=20)),
                ("address", models.TextField()),
                ("area", models.CharField(blank=True, max_length=120)),
                ("preferred_date", models.DateField(blank=True, null=True)),
                ("payment_method", models.CharField(choices=[("cod", "Cash on delivery"), ("upi", "UPI (confirm details on WhatsApp)")], default="cod", max_length=10)),
                ("notes", models.TextField(blank=True)),
                ("items_json", models.JSONField(default=list)),
                ("total", models.PositiveIntegerField(default=0)),
                ("status", models.CharField(choices=[("new", "New"), ("confirmed", "Confirmed"), ("completed", "Completed"), ("cancelled", "Cancelled")], default="new", max_length=20)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
