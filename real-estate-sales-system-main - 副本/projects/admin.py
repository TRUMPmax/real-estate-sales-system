from django.contrib import admin
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'developer', 'total_buildings', 'total_units', 'created_by', 'created_at']
    list_filter = ['created_at', 'developer']
    search_fields = ['name', 'address', 'developer']
    readonly_fields = ['created_at', 'updated_at']

