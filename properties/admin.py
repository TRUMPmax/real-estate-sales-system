from django.contrib import admin
from .models import Property, PriceHistory


class PriceHistoryInline(admin.TabularInline):
    model = PriceHistory
    extra = 0
    readonly_fields = ['changed_at', 'changed_by']


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'project', 'building_area', 'unit_price', 'total_price', 'status', 'created_at']
    list_filter = ['status', 'project', 'created_at']
    search_fields = ['project__name', 'building_number', 'unit_number', 'room_number']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [PriceHistoryInline]


@admin.register(PriceHistory)
class PriceHistoryAdmin(admin.ModelAdmin):
    list_display = ['property', 'unit_price', 'total_price', 'changed_by', 'changed_at']
    list_filter = ['changed_at']
    readonly_fields = ['changed_at']

