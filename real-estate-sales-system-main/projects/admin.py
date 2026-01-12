from django.contrib import admin
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'developer',
                    'total_buildings', 'units_per_building', 'floors_per_unit',
                    'created_by', 'created_at']
    list_filter = ['created_at', 'developer']
    search_fields = ['name', 'address', 'developer']
    readonly_fields = ['created_at', 'updated_at']

    # 字段分组显示
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'address', 'developer', 'description')
        }),
        ('项目配置', {
            'fields': ('total_buildings', 'units_per_building', 'floors_per_unit')
        }),
        ('其他信息', {
            'fields': ('construction_area',),
            'classes': ('collapse',)
        }),
        ('系统信息', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )