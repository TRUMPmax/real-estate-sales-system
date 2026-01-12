from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from .forms import LoginForm, UserCreateForm, UserUpdateForm, RegisterForm

User = get_user_model()


def login_view(request):
    """用户登录"""
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # 获取next参数，如果有则重定向到next，否则重定向到dashboard
            next_url = request.GET.get('next', 'accounts:dashboard')
            return redirect(next_url)
        else:
            # 表单验证失败，显示错误信息
            if form.non_field_errors():
                for error in form.non_field_errors():
                    messages.error(request, error)
            else:
                messages.error(request, '请检查输入的用户名和密码')
    else:
        form = LoginForm(request)
    
    return render(request, 'accounts/login.html', {'form': form})


def register_view(request):
    """用户注册 - 仅限购房者"""
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'注册成功！欢迎 {user.username}，请登录')
            return redirect('accounts:login')
    else:
        form = RegisterForm()
    
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def dashboard(request):
    """用户仪表板 - 根据角色显示不同内容"""
    user = request.user
    context = {
        'user': user,
    }
    
    if user.is_admin():
        # 管理员仪表板
        total_users = User.objects.count()
        context.update({
            'total_users': total_users,
        })
        return render(request, 'accounts/admin_dashboard.html', context)
    elif user.is_manager():
        # 销售经理仪表板
        from projects.models import Project
        from properties.models import Property
        total_projects = Project.objects.count()
        total_properties = Property.objects.count()
        context.update({
            'total_projects': total_projects,
            'total_properties': total_properties,
        })
        return render(request, 'accounts/manager_dashboard.html', context)
    elif user.is_salesperson():
        # 业务员仪表板
        from customers.models import Customer
        from sales.models import Sale
        total_customers = Customer.objects.filter(salesperson=user).count()
        total_sales = Sale.objects.filter(salesperson=user).count()
        context.update({
            'total_customers': total_customers,
            'total_sales': total_sales,
        })
        return render(request, 'accounts/salesperson_dashboard.html', context)
    else:
        # 购房者仪表板
        from properties.models import Property
        properties = Property.objects.filter(status='available')[:10]
        context.update({
            'properties': properties,
        })
        return render(request, 'accounts/buyer_dashboard.html', context)


@login_required
def user_list(request):
    """用户列表 - 仅管理员可访问"""
    if not request.user.is_admin():
        messages.error(request, '您没有权限访问此页面')
        return redirect('accounts:dashboard')
    
    users = User.objects.all()
    
    # 搜索功能
    search = request.GET.get('search', '')
    if search:
        users = users.filter(username__icontains=search) | users.filter(email__icontains=search)
    
    # 角色筛选
    role_filter = request.GET.get('role', '')
    if role_filter:
        users = users.filter(role=role_filter)
    
    paginator = Paginator(users, 20)
    page = request.GET.get('page')
    users = paginator.get_page(page)
    
    return render(request, 'accounts/user_list.html', {
        'users': users,
        'search': search,
        'role_filter': role_filter,
    })


@login_required
def user_create(request):
    """创建用户 - 仅管理员可访问"""
    if not request.user.is_admin():
        messages.error(request, '您没有权限访问此页面')
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'用户 {user.username} 创建成功')
            return redirect('accounts:user_list')
    else:
        form = UserCreateForm()
    
    return render(request, 'accounts/user_form.html', {
        'form': form,
        'title': '创建用户',
    })


@login_required
def user_update(request, pk):
    """更新用户 - 仅管理员可访问"""
    if not request.user.is_admin():
        messages.error(request, '您没有权限访问此页面')
        return redirect('accounts:dashboard')
    
    user = User.objects.get(pk=pk)
    
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f'用户 {user.username} 更新成功')
            return redirect('accounts:user_list')
    else:
        form = UserUpdateForm(instance=user)
    
    return render(request, 'accounts/user_form.html', {
        'form': form,
        'title': '更新用户',
        'user': user,
    })


@login_required
def user_delete(request, pk):
    """删除用户 - 仅管理员可访问"""
    if not request.user.is_admin():
        messages.error(request, '您没有权限访问此页面')
        return redirect('accounts:dashboard')
    
    user = User.objects.get(pk=pk)
    if request.method == 'POST':
        username = user.username
        user.delete()
        messages.success(request, f'用户 {username} 已删除')
        return redirect('accounts:user_list')
    
    return render(request, 'accounts/user_confirm_delete.html', {'user': user})

