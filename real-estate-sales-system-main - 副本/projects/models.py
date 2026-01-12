from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Project(models.Model):
    """项目/楼盘模型"""
    name = models.CharField(max_length=200, verbose_name='项目名称')
    address = models.CharField(max_length=500, verbose_name='地址')
    developer = models.CharField(max_length=200, verbose_name='开发商')
    description = models.TextField(blank=True, verbose_name='项目描述')
    total_buildings = models.IntegerField(default=0, verbose_name='总楼栋数')
    total_units = models.IntegerField(default=0, verbose_name='总户数')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_projects', verbose_name='创建人')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '项目'
        verbose_name_plural = '项目'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name

