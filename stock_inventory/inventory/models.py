from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class AddProduct(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    whole_sale = models.DecimalField(max_digits=10, decimal_places=2)
    retail_sale = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    
    def in_stock(self):
        return self.quantity > 0