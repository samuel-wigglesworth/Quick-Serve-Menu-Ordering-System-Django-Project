from django.db import models

from orders.models import Order


class DeliveryStatus(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="delivery_status")
    rider_name = models.CharField(max_length=100, blank=True)
    current_location = models.CharField(max_length=255, blank=True)
    eta = models.CharField(max_length=50, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Delivery #{self.order_id}"
