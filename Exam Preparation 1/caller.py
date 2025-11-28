import os
import django
from django.db.models import Q, F, Count

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import *
# Create queries within functions

def get_profiles(search_string=None):
    if search_string is not None:
        matches = Profile.objects.filter(
            Q(full_name__icontains=search_string) |
            Q(email__icontains=search_string) |
            Q(phone_number__icontains=search_string)).order_by('full_name')


        return '\n'.join([f"Profile: {m.full_name}, email: {m.email}, phone number: {m.phone_number}, orders: {m.orders.count()}"for m in matches])
    return None


def get_loyal_profiles():
    return '\n'.join([f"Profile: {p.full_name}, orders: {p.order_count}"for p in Profile.objects.get_regular_customers()])

def get_last_sold_products():
    last_order = Order.objects.last()
    last_prods = last_order.products.all()

    return f"Last sold products: {', '.join(p.name for p in last_prods)}"


def get_top_products():
    orders = Product.objects.annotate(num_orders=Count('orders')).order_by("-num_orders")[:5]
    return "Top Products: \n" + "\n".join([f"{r.name}, sold {r.num_orders} times"for r in orders])


def apply_discounts():
    orders_to_discount = Order.objects.annotate(
        num_products=Count('products')).filter(
        num_products__gt=2,
        is_completed=False,
    )

    orders_to_discount.update(total_price=F('total_price') * 0.9)
    return f"Discount applied to {len(orders_to_discount)} orders."


print(apply_discounts())

def complete_order():
    first_order = Order.objects.filter(is_completed=False).first()

    if not first_order:
        return ""

    first_order.products.update(in_stock=F('in_stock') - 1)
    if first_order.products.filter(in_stock=0):
        first_order.products.filter(in_stock=0).update(is_available=False)

    return "Order has been completed!"
