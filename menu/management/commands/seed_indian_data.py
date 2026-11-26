"""
Management command: seed_indian_data

Seeds the database with Indian-themed sample data:
  - 12 MenuItem records
  - 5 customer users + 1 staff/superuser
  - 3 sample Orders with OrderItems
  - 3 DeliveryStatus records with Indian city locations

Usage:
    python manage.py seed_indian_data           # idempotent seed
    python manage.py seed_indian_data --clear   # wipe existing data first
"""

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from customers.models import CustomerProfile
from delivery.models import DeliveryStatus
from menu.models import MenuItem
from orders.models import Order, OrderItem

User = get_user_model()


MENU_ITEMS = [
    {
        "name": "Butter Chicken",
        "description": "Tender chicken in rich tomato-cream sauce",
        "price": "350.00",
        "image_url": "https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=400",
    },
    {
        "name": "Dal Makhani",
        "description": "Slow-cooked black lentils with butter and cream",
        "price": "220.00",
        "image_url": "https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=400",
    },
    {
        "name": "Paneer Tikka",
        "description": "Grilled cottage cheese with tandoor spices",
        "price": "280.00",
        "image_url": "https://images.unsplash.com/photo-1567188040759-fb8a883dc6d6?w=400",
    },
    {
        "name": "Biryani (Hyderabadi)",
        "description": "Fragrant basmati rice with spiced meat and saffron",
        "price": "420.00",
        "image_url": "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=400",
    },
    {
        "name": "Masala Dosa",
        "description": "Crispy rice crepe with spiced potato filling",
        "price": "180.00",
        "image_url": "https://images.unsplash.com/photo-1668236543090-82eba5ee5976?w=400",
    },
    {
        "name": "Chole Bhature",
        "description": "Spicy chickpeas with fluffy fried bread",
        "price": "160.00",
        "image_url": "https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?w=400",
    },
    {
        "name": "Gulab Jamun",
        "description": "Soft milk-solid dumplings in rose syrup",
        "price": "120.00",
        "image_url": "https://images.unsplash.com/photo-1601050690597-df0568f70950?w=400",
    },
    {
        "name": "Mango Lassi",
        "description": "Chilled yoghurt drink with Alphonso mango",
        "price": "90.00",
        "image_url": "https://images.unsplash.com/photo-1527661591475-527312dd65f5?w=400",
    },
    {
        "name": "Palak Paneer",
        "description": "Cottage cheese in spiced spinach gravy",
        "price": "260.00",
        "image_url": "https://images.unsplash.com/photo-1604908176997-125f25cc6f3d?w=400",
    },
    {
        "name": "Samosa (2 pcs)",
        "description": "Crispy pastry filled with spiced potatoes and peas",
        "price": "60.00",
        "image_url": "https://images.unsplash.com/photo-1601050690597-df0568f70950?w=400",
    },
    {
        "name": "Tandoori Roti",
        "description": "Whole wheat bread baked in clay oven",
        "price": "40.00",
        "image_url": "https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=400",
    },
    {
        "name": "Kheer",
        "description": "Rice pudding with cardamom and pistachios",
        "price": "100.00",
        "image_url": "https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=400",
    },
]

CUSTOMERS = [
    {
        "username": "arjun.sharma",
        "first_name": "Arjun",
        "last_name": "Sharma",
        "email": "arjun.sharma@example.in",
        "password": "Test@1234",
        "phone": "+91 98765 43210",
        "address": "Mumbai, Maharashtra",
    },
    {
        "username": "priya.patel",
        "first_name": "Priya",
        "last_name": "Patel",
        "email": "priya.patel@example.in",
        "password": "Test@1234",
        "phone": "+91 98765 43211",
        "address": "Ahmedabad, Gujarat",
    },
    {
        "username": "rahul.verma",
        "first_name": "Rahul",
        "last_name": "Verma",
        "email": "rahul.verma@example.in",
        "password": "Test@1234",
        "phone": "+91 98765 43212",
        "address": "Delhi",
    },
    {
        "username": "sneha.nair",
        "first_name": "Sneha",
        "last_name": "Nair",
        "email": "sneha.nair@example.in",
        "password": "Test@1234",
        "phone": "+91 98765 43213",
        "address": "Kochi, Kerala",
    },
    {
        "username": "vikram.singh",
        "first_name": "Vikram",
        "last_name": "Singh",
        "email": "vikram.singh@example.in",
        "password": "Test@1234",
        "phone": "+91 98765 43214",
        "address": "Jaipur, Rajasthan",
    },
]

STAFF_USER = {
    "username": "admin",
    "email": "admin@quickserve.in",
    "password": "Admin@1234",
    "first_name": "Admin",
    "last_name": "QuickServe",
    "is_staff": True,
    "is_superuser": True,
}

# (customer_username, [(item_name, qty), ...], status, rider, location, eta)
SAMPLE_ORDERS = [
    (
        "arjun.sharma",
        [("Butter Chicken", 1), ("Tandoori Roti", 2), ("Mango Lassi", 1)],
        Order.Status.DELIVERED,
        "Rajan Kumar",
        "Andheri West, Mumbai",
        "Delivered",
    ),
    (
        "priya.patel",
        [("Paneer Tikka", 1), ("Dal Makhani", 1), ("Gulab Jamun", 2)],
        Order.Status.DISPATCHED,
        "Suresh Yadav",
        "Satellite Road, Ahmedabad",
        "30 mins",
    ),
    (
        "rahul.verma",
        [("Biryani (Hyderabadi)", 1), ("Samosa (2 pcs)", 2), ("Mango Lassi", 1)],
        Order.Status.PREPARING,
        "Deepak Sharma",
        "Connaught Place, Delhi",
        "45 mins",
    ),
]


class Command(BaseCommand):
    help = "Seed the database with Indian-themed sample data."

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Delete all existing MenuItem, Order, OrderItem, DeliveryStatus, and non-superuser User records before seeding.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options["clear"]:
            self.stdout.write("🗑️  Clearing existing data …")
            DeliveryStatus.objects.all().delete()
            OrderItem.objects.all().delete()
            Order.objects.all().delete()
            MenuItem.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()
            self.stdout.write(self.style.WARNING("   Existing data removed."))

        # ── Menu items ────────────────────────────────────────────────────────
        self.stdout.write("\n🍽️  Seeding menu items …")
        item_objects = {}
        created_count = 0
        for data in MENU_ITEMS:
            obj, created = MenuItem.objects.get_or_create(
                name=data["name"],
                defaults={
                    "description": data["description"],
                    "price": data["price"],
                    "image_url": data["image_url"],
                    "is_available": True,
                },
            )
            item_objects[obj.name] = obj
            if created:
                created_count += 1
                self.stdout.write(f"   ✅ Created: {obj.name}")
            else:
                self.stdout.write(f"   ⏭️  Exists:  {obj.name}")
        self.stdout.write(
            self.style.SUCCESS(f"   {created_count} item(s) created, {len(MENU_ITEMS) - created_count} already existed.")
        )

        # ── Staff user ────────────────────────────────────────────────────────
        self.stdout.write("\n👤  Seeding staff user …")
        staff_user, created = User.objects.get_or_create(
            username=STAFF_USER["username"],
            defaults={
                "email": STAFF_USER["email"],
                "first_name": STAFF_USER["first_name"],
                "last_name": STAFF_USER["last_name"],
                "is_staff": STAFF_USER["is_staff"],
                "is_superuser": STAFF_USER["is_superuser"],
            },
        )
        if created:
            staff_user.set_password(STAFF_USER["password"])
            staff_user.save()
            self.stdout.write(f"   ✅ Created staff user: {staff_user.username}")
        else:
            self.stdout.write(f"   ⏭️  Exists:  {staff_user.username}")

        # ── Customer users ────────────────────────────────────────────────────
        self.stdout.write("\n👥  Seeding customer users …")
        customer_objects = {}
        for cdata in CUSTOMERS:
            user, created = User.objects.get_or_create(
                username=cdata["username"],
                defaults={
                    "first_name": cdata["first_name"],
                    "last_name": cdata["last_name"],
                    "email": cdata["email"],
                },
            )
            if created:
                user.set_password(cdata["password"])
                user.save()
                self.stdout.write(f"   ✅ Created user: {user.username}")
            else:
                self.stdout.write(f"   ⏭️  Exists:  {user.username}")

            # Ensure CustomerProfile exists
            profile, _ = CustomerProfile.objects.get_or_create(
                user=user,
                defaults={
                    "phone": cdata["phone"],
                    "address": cdata["address"],
                },
            )
            customer_objects[user.username] = user

        # ── Sample orders ─────────────────────────────────────────────────────
        self.stdout.write("\n📦  Seeding sample orders …")
        for username, lines, status, rider, location, eta in SAMPLE_ORDERS:
            customer_user = customer_objects.get(username)
            if customer_user is None:
                self.stdout.write(self.style.WARNING(f"   ⚠️  User {username} not found, skipping order."))
                continue

            # Check whether this customer already has an order with the same
            # status to keep the command idempotent across re-runs.
            if Order.objects.filter(customer=customer_user, status=status).exists():
                self.stdout.write(f"   ⏭️  Order for {username} ({status}) already exists.")
                continue

            order = Order.objects.create(customer=customer_user, status=status)
            for item_name, qty in lines:
                menu_item = item_objects.get(item_name)
                if menu_item is None:
                    # Try fetching from DB in case it existed before seeding
                    try:
                        menu_item = MenuItem.objects.get(name=item_name)
                        item_objects[item_name] = menu_item
                    except MenuItem.DoesNotExist:
                        self.stdout.write(self.style.WARNING(f"   ⚠️  MenuItem '{item_name}' not found, skipping line."))
                        continue
                OrderItem.objects.create(order=order, menu_item=menu_item, quantity=qty)

            # Delivery record
            DeliveryStatus.objects.get_or_create(
                order=order,
                defaults={
                    "rider_name": rider,
                    "current_location": location,
                    "eta": eta,
                },
            )
            self.stdout.write(f"   ✅ Order #{order.pk} for {username} ({status})")

        self.stdout.write("\n" + self.style.SUCCESS("🎉  Seeding complete!"))
