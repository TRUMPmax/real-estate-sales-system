from django.contrib import admin
from .models import Sale


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['customer', 'property', 'salesperson', 'sale_price', 'status', 'contract_date', 'created_at']
    list_filter = ['status', 'created_at', 'salesperson']
    search_fields = ['customer__name', 'property__project__name', 'contract_number']
    readonly_fields = ['created_at', 'updated_at']

