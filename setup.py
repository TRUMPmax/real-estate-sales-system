"""
快速设置脚本
运行此脚本可以快速初始化数据库和创建管理员用户
"""
import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HSystem.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def create_admin():
    """创建管理员用户"""
    username = input('请输入管理员用户名 (默认: admin): ') or 'admin'
    email = input('请输入管理员邮箱 (默认: admin@example.com): ') or 'admin@example.com'
    password = input('请输入管理员密码: ')
    
    if not password:
        print('密码不能为空！')
        return
    
    if User.objects.filter(username=username).exists():
        print(f'用户 {username} 已存在！')
        return
    
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        role='admin',
        is_staff=True,
        is_superuser=True
    )
    
    print(f'管理员用户 {username} 创建成功！')

if __name__ == '__main__':
    print('=' * 50)
    print('房地产销售管理系统 - 初始化脚本')
    print('=' * 50)
    print()
    print('请确保已经完成以下步骤：')
    print('1. 安装依赖: pip install -r requirements.txt')
    print('2. 配置数据库连接 (HSystem/settings.py)')
    print('3. 创建数据库: mysql -u root -p < init_db.sql')
    print('4. 运行迁移: python manage.py makemigrations')
    print('5. 运行迁移: python manage.py migrate')
    print()
    
    choice = input('是否创建管理员用户？(y/n): ')
    if choice.lower() == 'y':
        create_admin()
    
    print()
    print('初始化完成！')
    print('运行 python manage.py runserver 启动开发服务器')

