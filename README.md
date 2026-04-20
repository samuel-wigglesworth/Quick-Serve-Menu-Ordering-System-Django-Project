# Quick Serve Menu Ordering System (Django)

This project is a Django-based platform for online food ordering and restaurant operations.

## Modules Included

- Login (signup, login, logout)
- Menu (public listing + staff menu management)
- Orders (place order, history, staff status update)
- Customers (customer profile management)
- Delivery Tracking (customer tracking + staff delivery updates)
- Reports (staff sales and top items report)

## Run Locally

1. Install dependencies:
   - `python -m pip install -r requirements.txt`
2. Apply migrations:
   - `python manage.py migrate`
3. Create admin user (optional but recommended):
   - `python manage.py createsuperuser`
4. Start server:
   - `python manage.py runserver`

## Main URLs

- `/accounts/login/`
- `/accounts/signup/`
- `/menu/`
- `/orders/create/`
- `/orders/history/`
- `/customers/profile/`
- `/reports/sales/` (staff only)
