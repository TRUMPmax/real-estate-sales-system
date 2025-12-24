"""
测试数据库连接脚本
运行此脚本可以测试MySQL数据库连接是否正常
"""
import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HSystem.settings')
django.setup()

from django.db import connection

try:
    # 测试数据库连接
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        print("✓ 数据库连接成功！")
        print(f"  数据库: {connection.settings_dict['NAME']}")
        print(f"  用户: {connection.settings_dict['USER']}")
        print(f"  主机: {connection.settings_dict['HOST']}")
        print(f"  端口: {connection.settings_dict['PORT']}")
except Exception as e:
    print("✗ 数据库连接失败！")
    print(f"  错误信息: {e}")
    print("\n请检查以下配置：")
    print("1. MySQL服务是否已启动")
    print("2. 数据库 'real_estate_system' 是否已创建")
    print("3. 用户名和密码是否正确")
    print("4. 用户是否有访问权限")
    sys.exit(1)

