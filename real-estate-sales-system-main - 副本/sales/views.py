from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth import get_user_model
from .models import Sale
from .forms import SaleForm
from properties.models import Property
from customers.models import Customer
# sales/views.py 中的 sale_list 函数
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Sale


User = get_user_model()


def is_salesperson_or_admin(user):
    """检查用户是否为业务员或管理员"""
    return user.is_authenticated and (user.is_salesperson() or user.is_admin())


# sales/views.py 中的 sale_list 函数
@login_required
def sale_list(request):
    """销售记录列表"""
    # 权限检查
    if not request.user.is_salesperson() and not request.user.is_admin():
        messages.error(request, '您没有权限访问此页面')
        return redirect('accounts:dashboard')

    # 获取所有销售记录（业务员只能看到自己的，管理员可以看到所有）
    if request.user.is_salesperson():
        sales = Sale.objects.filter(salesperson=request.user)
    else:
        sales = Sale.objects.all()

    # 基础搜索
    search = request.GET.get('search', '')
    if search:
        sales = sales.filter(
            Q(customer__name__icontains=search) |
            Q(property__project__name__icontains=search) |
            Q(contract_number__icontains=search)
        )

    # 状态筛选
    status_filter = request.GET.get('status', '')
    if status_filter:
        sales = sales.filter(status=status_filter)

    # 房源位置筛选
    building = request.GET.get('building', '')
    if building:
        sales = sales.filter(property__building_number=building)

    unit = request.GET.get('unit', '')
    if unit:
        sales = sales.filter(property__unit_number=unit)

    room = request.GET.get('room', '')
    if room:
        sales = sales.filter(property__room_number=room)

    # 获取所有可选值（用于下拉框）
    all_sales = Sale.objects.all()
    building_list = all_sales.values_list('property__building_number', flat=True).distinct().order_by(
        'property__building_number')
    unit_list = all_sales.values_list('property__unit_number', flat=True).distinct().order_by('property__unit_number')
    room_list = all_sales.values_list('property__room_number', flat=True).distinct().order_by('property__room_number')

    # 排序和分页
    sales = sales.order_by('-created_at')
    paginator = Paginator(sales, 20)
    page = request.GET.get('page')
    sales_page = paginator.get_page(page)

    context = {
        'sales': sales_page,
        'search': search,
        'status': status_filter,
        'building': building,
        'unit': unit,
        'room': room,
        'building_list': building_list,
        'unit_list': unit_list,
        'room_list': room_list,
    }

    return render(request, 'sales/sale_list.html', context)


@login_required
@user_passes_test(is_salesperson_or_admin)
def sale_create(request):
    """创建销售记录"""
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            sale = form.save(commit=False)
            # 如果是业务员创建，自动分配给自己
            if request.user.is_salesperson() and not sale.salesperson:
                sale.salesperson = request.user
            sale.save()

            # 更新房源状态为已预订
            if sale.property.status == 'available':
                sale.property.status = 'reserved'
                sale.property.save()

            messages.success(request, '销售记录创建成功')
            return redirect('sales:sale_list')
    else:
        form = SaleForm()
        # 如果是业务员，默认分配给自己
        if request.user.is_salesperson():
            form.fields['salesperson'].initial = request.user

    return render(request, 'sales/sale_form.html', {
        'form': form,
        'title': '创建销售记录',
    })


@login_required
@user_passes_test(is_salesperson_or_admin)
def sale_update(request, pk):
    """更新销售记录"""
    sale = get_object_or_404(Sale, pk=pk)

    # 业务员只能修改自己的销售记录
    if request.user.is_salesperson() and sale.salesperson != request.user:
        messages.error(request, '您没有权限修改此销售记录')
        return redirect('sales:sale_list')

    if request.method == 'POST':
        form = SaleForm(request.POST, instance=sale)
        if form.is_valid():
            form.save()
            messages.success(request, '销售记录更新成功')
            return redirect('sales:sale_list')
    else:
        form = SaleForm(instance=sale)

    return render(request, 'sales/sale_form.html', {
        'form': form,
        'title': '更新销售记录',
        'sale': sale,
    })


@login_required
def sale_detail(request, pk):
    """销售记录详情"""
    sale = get_object_or_404(Sale, pk=pk)

    # 业务员只能查看自己的销售记录
    if request.user.is_salesperson() and sale.salesperson != request.user:
        messages.error(request, '您没有权限查看此销售记录')
        return redirect('sales:sale_list')

    return render(request, 'sales/sale_detail.html', {
        'sale': sale,
    })


@login_required
@user_passes_test(is_salesperson_or_admin)
def sale_delete(request, pk):
    """删除销售记录"""
    sale = get_object_or_404(Sale, pk=pk)

    # 业务员只能删除自己的销售记录
    if request.user.is_salesperson() and sale.salesperson != request.user:
        messages.error(request, '您没有权限删除此销售记录')
        return redirect('sales:sale_list')

    if request.method == 'POST':
        # 如果删除，恢复房源状态
        if sale.property.status in ['reserved', 'sold']:
            sale.property.status = 'available'
            sale.property.save()

        sale.delete()
        messages.success(request, '销售记录已删除')
        return redirect('sales:sale_list')

    return render(request, 'sales/sale_confirm_delete.html', {'sale': sale})

