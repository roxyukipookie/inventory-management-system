from django.db import models
from dashboard.models import Product
from django.utils import timezone

class Sales_History(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_sold = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Sale of {self.product.name} ({self.quantity_sold} units)"

