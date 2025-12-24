"""
创建管理员用户脚本
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HSystem.settings')
django.setup()

from accounts.models import User

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
        choice = input('是否更新密码？(y/n): ')
        if choice.lower() == 'y':
            user = User.objects.get(username=username)
            user.set_password(password)
            user.role = 'admin'
            user.is_staff = True
            user.is_superuser = True
            user.save()
            print(f'用户 {username} 密码已更新！')
        return
    
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        role='admin',
        is_staff=True,
        is_superuser=True
    )
    
    print(f'\n管理员用户 {username} 创建成功！')
    print(f'用户名: {username}')
    print(f'邮箱: {email}')
    print(f'角色: 管理员')

if __name__ == '__main__':
    try:
        create_admin()
    except KeyboardInterrupt:
        print('\n\n操作已取消')
    except Exception as e:
        print(f'\n错误: {e}')

