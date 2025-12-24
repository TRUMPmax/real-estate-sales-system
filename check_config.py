"""
检查数据库配置
"""
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HSystem.settings')

import django
django.setup()

from django.conf import settings

print("数据库配置信息：")
print(f"  ENGINE: {settings.DATABASES['default']['ENGINE']}")
print(f"  NAME: {settings.DATABASES['default']['NAME']}")
print(f"  USER: {settings.DATABASES['default']['USER']}")
print(f"  PASSWORD: {'*' * len(settings.DATABASES['default']['PASSWORD']) if settings.DATABASES['default']['PASSWORD'] else '(空)'}")
print(f"  PASSWORD长度: {len(settings.DATABASES['default']['PASSWORD'])}")
print(f"  HOST: {settings.DATABASES['default']['HOST']}")
print(f"  PORT: {settings.DATABASES['default']['PORT']}")

