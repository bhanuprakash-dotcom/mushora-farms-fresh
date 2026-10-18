# Mushora Farms — Django website

This project keeps the existing Mushora Farms storefront design and adds:
- Customer registration and login (`/accounts/register/`, `/accounts/login/`)
- Customer-only order history (`/my-orders/`)
- Separate staff/admin sign-in (`/manage/login/`, with `/admin/` retained as an alias)
- Product image uploads, editable prices, and in-stock/out-of-stock controls
- Editable public contact and WhatsApp numbers in Website settings
- Customer orders linked to the signed-in account

## Important before replacing project files

This updated ZIP intentionally does not include `db.sqlite3`, to avoid overwriting existing product or order data. Copy the updated source files into your existing project folder and keep your current database file. Back up the database before deploying migrations.

## Local setup

Use Python 3.11 or 3.12. From this project folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

On Windows, use `py -m venv .venv`, activate `.venv\\Scripts\\activate`, and run `python` in place of `python3`.

Open `http://127.0.0.1:8000/`. Sign in to the staff dashboard at `http://127.0.0.1:8000/manage/login/`. The first staff account is created with `createsuperuser`.

## Give your partner a separate admin login

1. Sign in to the admin dashboard with the superuser account.
2. Open **Users** and add a new user for your partner.
3. Set a strong password, then enable **Staff status**. Give only the permissions they need.
4. They can sign in separately at `/manage/login/`.

Do not share the superuser password. Customers use `/accounts/register/` and `/accounts/login/`; customer accounts cannot access the admin dashboard.

## Manage the storefront

In the staff dashboard:
- **Products**: change price and pack size, edit descriptions, upload a product photo, and toggle availability. An unavailable product remains visible with an “Out of stock” label and cannot be ordered.
- **Website settings**: update the customer-facing phone number and WhatsApp number. Enter the WhatsApp number with country code and digits only, e.g. `919550957029`.
- **Orders**: review customer details and update order status.

The first homepage visit creates the three example products if no products exist. Confirm prices and product descriptions before taking real orders.

## Deploying updates to Render

After uploading these files to your GitHub repository, trigger a new Render deploy. Ensure your Render build command installs requirements and applies migrations:

```bash
pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
```

Keep your `DJANGO_SECRET_KEY` secret in Render environment variables. Set `DEBUG=False`. `ALLOWED_HOSTS` can include `mushora-farms-2.onrender.com` (or use the project's existing `.onrender.com` allowance). If your deployment uses a CSRF trusted-origin list, include `https://mushora-farms-2.onrender.com`.

**Important production storage note:** Render's default app filesystem is not guaranteed to preserve SQLite database changes or uploaded photos across deploys/restarts. Before relying on live customer orders and photo uploads, configure a persistent disk for the database and media, or use managed PostgreSQL plus persistent/cloud media storage. Do not delete or replace your existing live database without backing it up.

## Security and migration notes

- This update adds a nullable customer account link to existing orders, so existing orders are preserved but will not automatically appear in a customer's account history.
- New customer checkout requires login.
- Customer order details are restricted to the customer account that placed them.
- Use HTTPS and strong passwords for staff accounts.
