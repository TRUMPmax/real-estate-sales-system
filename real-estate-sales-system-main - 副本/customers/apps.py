# customers/apps.py
from django.apps import AppConfig


class CustomersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'customers'
    verbose_name = '客户管理'

    def ready(self):
        # 导入信号处理器
        import customers.signals