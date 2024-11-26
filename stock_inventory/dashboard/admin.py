from django.contrib import admin
from .models import Notification, Product, Profile

# Register your models here.
admin.site.register(Notification)
admin.site.register(Product)
admin.site.register(Profile)