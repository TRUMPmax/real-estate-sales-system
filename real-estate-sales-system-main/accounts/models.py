from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """用户模型 - 支持四类角色"""
    ROLE_CHOICES = [
        ('admin', '管理员'),
        ('manager', '销售经理'),
        ('salesperson', '业务员'),
        ('buyer', '购房者'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, verbose_name='角色')
    phone = models.CharField(max_length=20, blank=True, verbose_name='电话')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    def is_admin(self):
        return self.role == 'admin'
    
    def is_manager(self):
        return self.role == 'manager'
    
    def is_salesperson(self):
        return self.role == 'salesperson'
    
    def is_buyer(self):
        return self.role == 'buyer'

