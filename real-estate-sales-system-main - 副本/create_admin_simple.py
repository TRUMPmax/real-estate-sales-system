"""
创建管理员用户脚本（非交互式）
用法: python create_admin_simple.py [username] [email] [password]
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HSystem.settings')
django.setup()

from accounts.models import User

def create_admin(username='admin', email='admin@example.com', password='admin123'):
    """创建管理员用户"""
    if User.objects.filter(username=username).exists():
        print(f'用户 {username} 已存在，正在更新...')
        user = User.objects.get(username=username)
        user.set_password(password)
        user.email = email
        user.role = 'admin'
        user.is_staff = True
        user.is_superuser = True
        user.save()
        print(f'用户 {username} 已更新！')
    else:
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role='admin',
            is_staff=True,
            is_superuser=True
        )
        print(f'管理员用户 {username} 创建成功！')
    
    print(f'用户名: {username}')
    print(f'邮箱: {email}')
    print(f'密码: {password}')
    print(f'角色: 管理员')

if __name__ == '__main__':
    if len(sys.argv) >= 4:
        username = sys.argv[1]
        email = sys.argv[2]
        password = sys.argv[3]
    elif len(sys.argv) == 2:
        username = sys.argv[1]
        email = 'admin@example.com'
        password = 'admin123'
    else:
        username = 'admin'
        email = 'admin@example.com'
        password = 'admin123'
        print('使用默认参数创建管理员用户')
        print('如需自定义，请使用: python create_admin_simple.py [username] [email] [password]')
        print()
    
    try:
        create_admin(username, email, password)
        print('\n现在可以使用以下命令启动服务器:')
        print('python manage.py runserver')
    except Exception as e:
        print(f'\n错误: {e}')
        sys.exit(1)

