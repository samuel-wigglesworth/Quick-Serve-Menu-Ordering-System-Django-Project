# Quick Serve – Menu Ordering System

A restaurant menu ordering platform that lets customers browse the menu and place orders online, while staff manage orders, delivery status, and menu items in real time.

## Features

| Module | Description |
|---|---|
| Login / Signup | Customer and staff registration with role-based access |
| Menu | Browse available items with search and availability filter |
| Orders | Place multi-item orders; view full order history |
| Customers | Staff view of all registered customer accounts |
| Delivery Tracking | Visual step tracker with rider name, location, and ETA |
| Reports | Sales KPIs, top items chart, status breakdown |

## Project Structure

```
├── accounts/          Django accounts app (auth)
├── customers/         Customer profile model and views
├── delivery/          Delivery status model and views
├── menu/              Menu item model and views
├── orders/            Order and OrderItem models and views
├── reports/           Sales report view
├── quickserve/        Django project settings and root URLs
├── templates/         Django HTML templates
├── dist/              Static build – deploy this to Cloudflare Pages
│   ├── index.html     Dashboard
│   ├── login.html
│   ├── signup.html
│   ├── menu.html
│   ├── order-create.html
│   ├── order-detail.html
│   ├── order-manage.html
│   ├── orders.html
│   ├── delivery.html
│   ├── delivery-update.html
│   ├── menu-manage.html
│   ├── customers.html
│   ├── profile.html
│   ├── reports.html
│   ├── 404.html
│   ├── _redirects     Cloudflare Pages redirect rules
│   ├── css/styles.css
│   └── js/
│       ├── app.js     Data store, auth helpers, UI utilities
│       └── nav.js     Sidebar renderer
└── manage.py
```

## Running the Django Version Locally

```bash
pip install django
python manage.py migrate
python manage.py runserver
```

## Deploying to Cloudflare Pages (Static)

The `dist/` folder is a fully self-contained static app that requires no server.

### Option 1 – Drag and Drop

1. Go to [pages.cloudflare.com](https://pages.cloudflare.com)
2. Click **Create a project** → **Direct Upload**
3. Upload the contents of the `dist/` folder (or a zip of it)

### Option 2 – Connect GitHub Repository

1. Push this repository to GitHub
2. In Cloudflare Pages, click **Create a project** → **Connect to Git**
3. Select this repository
4. Set **Build output directory** to `dist`
5. Leave the build command blank (no build step needed)
6. Deploy

## Demo Credentials

| Role | Username | Password |
|---|---|---|
| Staff | `admin` | `admin123` |
| Customer | `john` | `pass123` |
| Customer | `sarah` | `pass123` |

Data is stored in `localStorage` — no backend or database required for the static version.

## Tech Stack

- **Static frontend:** Vanilla HTML, CSS, JavaScript (no frameworks)
- **Data persistence:** Browser `localStorage`
- **Django backend:** Python 3, Django 5, SQLite
