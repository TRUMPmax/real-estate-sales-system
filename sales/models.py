from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model
from properties.models import Property
from customers.models import Customer

User = get_user_model()


class Sale(models.Model):
    """销售记录模型"""
    STATUS_CHOICES = [
        ('pending', '待审核'),
        ('approved', '已批准'),
        ('completed', '已完成'),
        ('cancelled', '已取消'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='sales', verbose_name='客户')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='sales', verbose_name='房源')
    salesperson = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, 
                                   related_name='sales', limit_choices_to={'role': 'salesperson'},
                                   verbose_name='业务员')
    
    # 销售价格（可能与房源价格不同）
    sale_price = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)], verbose_name='成交价(元)')
    
    # 付款信息
    down_payment = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)], 
                                     default=0, verbose_name='首付款(元)')
    payment_method = models.CharField(max_length=100, blank=True, verbose_name='付款方式')
    
    # 合同信息
    contract_number = models.CharField(max_length=100, blank=True, verbose_name='合同编号')
    contract_date = models.DateField(null=True, blank=True, verbose_name='签约日期')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='状态')
    notes = models.TextField(blank=True, verbose_name='备注')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '销售记录'
        verbose_name_plural = '销售记录'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.customer.name} - {self.property}"
    
    def save(self, *args, **kwargs):
        # 如果销售完成，更新房源状态
        if self.status == 'completed' and self.property.status != 'sold':
            self.property.status = 'sold'
            self.property.save()
        super().save(*args, **kwargs)

