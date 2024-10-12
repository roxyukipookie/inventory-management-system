from django.db import models
from django.utils import timezone

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) 
    sold_quantity = models.PositiveIntegerField(default=0)  
    created_at = models.DateTimeField(default=timezone.now)
    alert_threshold = models.PositiveIntegerField(default=10)  # Minimum stock level before a product is considered 'low'

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        is_new_product = self.pk is None
        old_quantity = None

        # If the product already exists, get its current quantity
        if not is_new_product:
            old_quantity = Product.objects.get(pk=self.pk).quantity

        # Call the parent class's save method first
        super(Product, self).save(*args, **kwargs)

        # If this is a new product, create a notification
        if is_new_product:
            Notification.objects.create(
                title="New Product Added",
                message=f"A new product '{self.name}' has been added to the inventory.",
                notification_type='new-product',
                icon='img/shipped.png'  
            )
        else:
            # If the product quantity has increased (indicating stock replenishment)
            if old_quantity is not None and self.quantity > old_quantity:
                Notification.objects.create(
                    title="Stock Replenished",
                    message=f"The stock of '{self.name}' has been replenished. Now {self.quantity} in stock.",
                    notification_type='stock-replenished',
                    icon='img/reload.png'
                )

        # Check if product is out of stock
        if self.quantity == 0:
            # Create a new out-of-stock notification
            Notification.objects.create(
                title="0ut of stock",
                message=f"The product '{self.name}' has run out of stock.",
                notification_type='out-of-stock',
                icon='img/out.png'
            )
        
        # Check if product is low on stock (below alert threshold)
        elif self.quantity < self.alert_threshold:
            # Create a new low-stock notification
            Notification.objects.create(
                title="Low Stock",
                message=f"The stock level of '{self.name}' is below the threshold ({self.quantity} remaining).",
                notification_type='low-stock',
                icon='img/warning.svg'
            )

class Notification(models.Model):
    title = models.CharField(max_length=255, default='notification')
    related_product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE)
    message = models.TextField()
    icon = models.CharField(max_length=255, default='img/icon.png')  # URL or static path for the icon
    created_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)
    notification_type = models.CharField(max_length=50, default='general')  # e.g., 'low-stock', 'out-of-stock', 'new-stock'

    def __str__(self):
        return self.title
