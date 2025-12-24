from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model
from projects.models import Project

User = get_user_model()


class Property(models.Model):
    """房源模型"""
    STATUS_CHOICES = [
        ('available', '可售'),
        ('reserved', '已预订'),
        ('sold', '已售'),
        ('unavailable', '不可售'),
    ]
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='properties', verbose_name='所属项目')
    building_number = models.CharField(max_length=50, verbose_name='楼栋号')
    unit_number = models.CharField(max_length=50, verbose_name='单元号')
    room_number = models.CharField(max_length=50, verbose_name='房号')
    floor = models.IntegerField(verbose_name='楼层')
    
    # 面积信息
    building_area = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], verbose_name='建筑面积(㎡)')
    interior_area = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], verbose_name='套内面积(㎡)')
    shared_area = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], verbose_name='公摊面积(㎡)')
    
    # 价格信息
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)], verbose_name='单价(元/㎡)')
    total_price = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)], verbose_name='总价(元)')
    
    # 位置信息
    location_description = models.TextField(blank=True, verbose_name='位置描述')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available', verbose_name='状态')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_properties', verbose_name='创建人')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '房源'
        verbose_name_plural = '房源'
        ordering = ['-created_at']
        unique_together = ['project', 'building_number', 'unit_number', 'room_number']
    
    def __str__(self):
        return f"{self.project.name} - {self.building_number}-{self.unit_number}-{self.room_number}"
    
    def save(self, *args, **kwargs):
        # 自动计算总价
        if not self.total_price or self.total_price == 0:
            self.total_price = self.unit_price * self.building_area
        super().save(*args, **kwargs)


class PriceHistory(models.Model):
    """价格历史记录"""
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='price_history', verbose_name='房源')
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='单价(元/㎡)')
    total_price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='总价(元)')
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='修改人')
    changed_at = models.DateTimeField(auto_now_add=True, verbose_name='修改时间')
    reason = models.CharField(max_length=500, blank=True, verbose_name='调价原因')
    
    class Meta:
        verbose_name = '价格历史'
        verbose_name_plural = '价格历史'
        ordering = ['-changed_at']
    
    def __str__(self):
        return f"{self.property} - {self.changed_at}"

