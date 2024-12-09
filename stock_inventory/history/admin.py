from django.contrib import admin
from .models import Sales_History

@admin.register(Sales_History)
class SalesHistoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity_sold', 'total_price', 'sale_time')
    search_fields = ('product__name',)  # ASSUMING PRODUCT HAS A NAME FIELD
    list_filter = ('sale_time',)
