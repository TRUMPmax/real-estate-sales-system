"""
测试登录功能
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HSystem.settings')
django.setup()

from accounts.models import User
from django.contrib.auth import authenticate

# 检查用户是否存在
username = 'admin'
try:
    user = User.objects.get(username=username)
    print(f"[OK] 用户 {username} 存在")
    print(f"  - 邮箱: {user.email}")
    print(f"  - 角色: {user.get_role_display()}")
    print(f"  - 是否激活: {user.is_active}")
    print(f"  - 是否员工: {user.is_staff}")
    print(f"  - 是否超级用户: {user.is_superuser}")
    
    # 测试密码验证
    password = 'admin123'
    user_check = authenticate(username=username, password=password)
    if user_check:
        print(f"[OK] 密码验证成功")
    else:
        print(f"[ERROR] 密码验证失败")
        print(f"  尝试的密码: {password}")
        
        # 检查密码是否正确设置
        if user.check_password(password):
            print(f"  (用户对象的check_password返回True)")
        else:
            print(f"  (用户对象的check_password返回False)")
            print(f"  可能需要重置密码")
            
except User.DoesNotExist:
    print(f"[ERROR] 用户 {username} 不存在")

