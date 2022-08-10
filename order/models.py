from django.db import models
from django.utils import timezone
from user.models import User
from product.models import Product


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    total_amount = models.FloatField()
    is_delivered = models.BooleanField(default=False)
    is_deleted_by_user = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)
    delivery_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(blank=True, null=True)
    remarks = models.TextField(max_length=1000, default="")
  

class Item(models.Model):
    order = models.ForeignKey(Order, related_name='items',on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=100)
    price = models.FloatField()
    discount = models.FloatField(default=0)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

        