# customers/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

try:
    from sales.models import Sale


    @receiver(post_save, sender=Sale)
    def update_customer_purchase_status(sender, instance, **kwargs):
        """当销售记录保存时更新客户的购房状态"""
        if instance.customer:
            instance.customer.update_purchase_status()


    @receiver(post_delete, sender=Sale)
    def update_customer_purchase_status_on_delete(sender, instance, **kwargs):
        """当销售记录删除时更新客户的购房状态"""
        if instance.customer:
            instance.customer.update_purchase_status()
except ImportError:
    # 如果sales应用尚未创建，跳过
    pass