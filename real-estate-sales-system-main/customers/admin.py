from django.contrib import admin
from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'salesperson', 'created_at']
    list_filter = ['gender', 'created_at', 'salesperson']
    search_fields = ['name', 'phone', 'email', 'id_card']
    readonly_fields = ['created_at', 'updated_at']

