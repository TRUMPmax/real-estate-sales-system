# 快速启动指南

## 1. 环境准备

确保已安装：
- Python 3.8+
- MySQL 5.7+
- pip

## 2. 安装依赖

```bash
pip install -r requirements.txt
```

**注意**：项目已配置使用 `pymysql` 作为 MySQL 驱动（无需 Visual C++ 编译器）。配置已在 `HSystem/__init__.py` 中完成，无需额外设置。

## 3. 配置数据库

### 3.1 创建数据库

在MySQL中执行：
```sql
CREATE DATABASE real_estate_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

或者使用提供的SQL文件：
```bash
mysql -u root -p < init_db.sql
```

### 3.2 修改数据库配置

编辑 `HSystem/settings.py`，修改数据库连接信息：
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'real_estate_system',
        'USER': 'root',  # 修改为你的MySQL用户名
        'PASSWORD': 'your_password',  # 修改为你的MySQL密码
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

## 4. 初始化数据库

```bash
python manage.py makemigrations
python manage.py migrate
```

## 5. 创建管理员用户

### 方法1：使用Django命令
```bash
python manage.py createsuperuser
```
创建时，在Django shell中设置角色：
```python
python manage.py shell
>>> from accounts.models import User
>>> user = User.objects.get(username='admin')
>>> user.role = 'admin'
>>> user.save()
```

### 方法2：使用初始化脚本
```bash
python setup.py
```

## 6. 启动开发服务器

```bash
python manage.py runserver
```

访问 http://127.0.0.1:8000 即可使用系统。

## 7. 默认测试账号（可选）

可以在Django shell中创建测试账号：

```python
python manage.py shell
```

```python
from accounts.models import User

# 创建管理员
admin = User.objects.create_user('admin', 'admin@test.com', 'admin123', role='admin', is_staff=True, is_superuser=True)

# 创建销售经理
manager = User.objects.create_user('manager', 'manager@test.com', 'manager123', role='manager')

# 创建业务员
salesperson = User.objects.create_user('salesperson', 'sales@test.com', 'sales123', role='salesperson')

# 创建购房者
buyer = User.objects.create_user('buyer', 'buyer@test.com', 'buyer123', role='buyer')
```

## 8. 功能测试流程

1. **管理员登录** → 创建其他角色用户
2. **销售经理登录** → 创建项目 → 创建房源 → 管理价格
3. **业务员登录** → 创建客户 → 创建销售记录
4. **购房者登录** → 查询房源 → 登记信息

## 常见问题

### Q: 无法连接MySQL数据库
A: 检查MySQL服务是否启动，确认用户名密码正确，确保数据库已创建。

### Q: 静态文件无法加载
A: 运行 `python manage.py collectstatic` 收集静态文件。

### Q: 模板找不到
A: 确保 `templates` 目录在项目根目录下，检查 `settings.py` 中的 `TEMPLATES` 配置。

### Q: 权限错误
A: 确保用户角色设置正确，检查视图中的权限装饰器。

## 下一步

- 查看 `README.md` 了解详细功能说明
- 根据实际需求修改模型和视图
- 配置生产环境部署

