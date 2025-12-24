from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth import get_user_model
from .models import Customer
from .forms import CustomerForm

User = get_user_model()


def is_salesperson_or_admin(user):
    """检查用户是否为业务员或管理员"""
    return user.is_authenticated and (user.is_salesperson() or user.is_admin())


@login_required
def customer_list(request):
    """客户列表"""
    if request.user.is_salesperson():
        # 业务员只能看到自己的客户
        customers = Customer.objects.filter(salesperson=request.user)
    elif request.user.is_admin():
        # 管理员可以看到所有客户
        customers = Customer.objects.all()
    else:
        messages.error(request, '您没有权限访问此页面')
        return redirect('accounts:dashboard')
    
    # 搜索功能
    search = request.GET.get('search', '')
    if search:
        customers = customers.filter(
            Q(name__icontains=search) |
            Q(phone__icontains=search) |
            Q(email__icontains=search)
        )
    
    paginator = Paginator(customers, 20)
    page = request.GET.get('page')
    customers = paginator.get_page(page)
    
    return render(request, 'customers/customer_list.html', {
        'customers': customers,
        'search': search,
    })


@login_required
@user_passes_test(is_salesperson_or_admin)
def customer_create(request):
    """创建客户"""
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            # 如果是业务员创建，自动分配给自己
            if request.user.is_salesperson() and not customer.salesperson:
                customer.salesperson = request.user
            customer.save()
            messages.success(request, f'客户 {customer.name} 创建成功')
            return redirect('customers:customer_list')
    else:
        form = CustomerForm()
        # 如果是业务员，默认分配给自己
        if request.user.is_salesperson():
            form.fields['salesperson'].initial = request.user
    
    return render(request, 'customers/customer_form.html', {
        'form': form,
        'title': '创建客户',
    })


@login_required
@user_passes_test(is_salesperson_or_admin)
def customer_update(request, pk):
    """更新客户"""
    customer = get_object_or_404(Customer, pk=pk)
    
    # 业务员只能修改自己的客户
    if request.user.is_salesperson() and customer.salesperson != request.user:
        messages.error(request, '您没有权限修改此客户')
        return redirect('customers:customer_list')
    
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, f'客户 {customer.name} 更新成功')
            return redirect('customers:customer_list')
    else:
        form = CustomerForm(instance=customer)
    
    return render(request, 'customers/customer_form.html', {
        'form': form,
        'title': '更新客户',
        'customer': customer,
    })


@login_required
def customer_detail(request, pk):
    """客户详情"""
    customer = get_object_or_404(Customer, pk=pk)
    
    # 业务员只能查看自己的客户
    if request.user.is_salesperson() and customer.salesperson != request.user:
        messages.error(request, '您没有权限查看此客户')
        return redirect('customers:customer_list')
    
    from sales.models import Sale
    sales = Sale.objects.filter(customer=customer)
    
    return render(request, 'customers/customer_detail.html', {
        'customer': customer,
        'sales': sales,
    })


@login_required
@user_passes_test(is_salesperson_or_admin)
def customer_delete(request, pk):
    """删除客户"""
    customer = get_object_or_404(Customer, pk=pk)
    
    # 业务员只能删除自己的客户
    if request.user.is_salesperson() and customer.salesperson != request.user:
        messages.error(request, '您没有权限删除此客户')
        return redirect('customers:customer_list')
    
    if request.method == 'POST':
        name = customer.name
        customer.delete()
        messages.success(request, f'客户 {name} 已删除')
        return redirect('customers:customer_list')
    
    return render(request, 'customers/customer_confirm_delete.html', {'customer': customer})


@login_required
def customer_register(request):
    """购房者登记 - 公开访问"""
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            messages.success(request, '登记成功，我们会尽快与您联系')
            return redirect('customers:customer_register')
    else:
        form = CustomerForm()
    
    return render(request, 'customers/customer_register.html', {
        'form': form,
    })

