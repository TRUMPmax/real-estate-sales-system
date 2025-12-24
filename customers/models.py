from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Customer(models.Model):
    """客户模型"""
    GENDER_CHOICES = [
        ('M', '男'),
        ('F', '女'),
    ]
    
    name = models.CharField(max_length=100, verbose_name='姓名')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, verbose_name='性别')
    phone = models.CharField(max_length=20, verbose_name='电话')
    email = models.EmailField(blank=True, verbose_name='邮箱')
    id_card = models.CharField(max_length=18, blank=True, verbose_name='身份证号')
    address = models.CharField(max_length=500, blank=True, verbose_name='地址')
    notes = models.TextField(blank=True, verbose_name='备注')
    
    # 关联业务员
    salesperson = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                                    related_name='customers', limit_choices_to={'role': 'salesperson'},
                                    verbose_name='负责业务员')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '客户'
        verbose_name_plural = '客户'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.phone})"

