# 房地产销售管理系统

基于Django框架开发的房地产销售管理系统，使用MySQL数据库。

## 功能特性

### 用户角色
系统支持四类用户角色：
- **管理员**：用户管理和系统维护
- **销售经理**：房源管理、价格管理
- **业务员**：客户管理、销售管理
- **购房者**：房源查询、信息登记

### 主要功能模块

#### 1. 用户管理（管理员）
- 用户列表查看
- 用户创建、编辑、删除
- 用户角色分配
- 用户状态管理

#### 2. 项目管理（销售经理）
- 项目/楼盘信息管理
- 项目创建、编辑、删除
- 项目详情查看

#### 3. 房源管理（销售经理）
- 房源信息管理（位置、面积、价格等）
- 房源创建、编辑、删除
- 房源查询和筛选
- 价格管理和价格历史记录

#### 4. 客户管理（业务员）
- 客户信息管理
- 客户创建、编辑、删除
- 客户详情查看
- 购房者信息登记

#### 5. 销售管理（业务员）
- 销售记录管理
- 销售创建、编辑、删除
- 销售状态跟踪
- 合同信息管理

## 技术栈

- **后端框架**: Django 4.2.7
- **数据库**: MySQL
- **前端**: Bootstrap 5
- **表单**: Django Crispy Forms

## 安装和配置

### 1. 环境要求
- Python 3.8+
- MySQL 5.7+
- pip

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 数据库配置
在 `HSystem/settings.py` 中配置MySQL数据库连接：
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'real_estate_system',
        'USER': 'root',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 4. 创建数据库
在MySQL中创建数据库：
```sql
CREATE DATABASE real_estate_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 5. 数据库迁移
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. 创建超级用户
```bash
python manage.py createsuperuser
```

### 7. 运行开发服务器
```bash
python manage.py runserver
```

访问 http://127.0.0.1:8000 即可使用系统。

## 使用说明

### 创建用户
1. 使用管理员账号登录
2. 进入"用户管理"页面
3. 点击"创建用户"
4. 填写用户信息并选择角色

### 创建项目
1. 使用销售经理或管理员账号登录
2. 进入"项目管理"页面
3. 点击"创建项目"
4. 填写项目信息

### 创建房源
1. 使用销售经理或管理员账号登录
2. 进入"房源管理"页面
3. 点击"创建房源"
4. 选择项目并填写房源详细信息

### 管理客户
1. 使用业务员或管理员账号登录
2. 进入"客户管理"页面
3. 可以创建、编辑、查看客户信息

### 创建销售记录
1. 使用业务员或管理员账号登录
2. 进入"销售管理"页面
3. 点击"创建销售记录"
4. 选择客户和房源，填写销售信息

## 注意事项

1. 首次使用需要创建管理员账号
2. 确保MySQL服务已启动
3. 根据实际情况修改数据库配置
4. 生产环境请修改SECRET_KEY

## 许可证

MIT License

