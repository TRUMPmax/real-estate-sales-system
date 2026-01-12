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
from projects.models import Project  # 导入Project模型

User = get_user_model()


def is_salesperson_or_admin(user):
    """检查用户是否为业务员或管理员"""
    return user.is_authenticated and (user.is_salesperson() or user.is_admin())


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

    # 获取所有项目用于搜索
    projects = Project.objects.all()

    # 获取搜索参数
    search = request.GET.get('search', '')
    selected_project = request.GET.get('project', '')
    building = request.GET.get('building', '')
    unit = request.GET.get('unit', '')
    floor = request.GET.get('floor', '')
    room = request.GET.get('room', '')
    status_filter = request.GET.get('status', '')

    # 基础搜索
    if search:
        sales = sales.filter(
            Q(customer__name__icontains=search) |
            Q(property__project__name__icontains=search) |
            Q(contract_number__icontains=search)
        )

    # 项目筛选
    if selected_project:
        sales = sales.filter(property__project_id=selected_project)

    # 房源位置筛选 - 处理带单位的搜索
    if building:
        # 处理格式：可能是 "1" 或 "1栋"
        building_clean = str(building).strip()
        # 提取数字部分
        import re
        building_match = re.search(r'\d+', building_clean)
        if building_match:
            building_number = building_match.group()  # 提取数字
            # 搜索数据库中的纯数字或带"栋"的格式
            sales = sales.filter(
                Q(property__building_number=building_number) |
                Q(property__building_number=building_number + "栋") |
                Q(property__building_number="栋" + building_number)
            )
            print(f"DEBUG - 搜索栋号: 输入='{building_clean}', 提取数字='{building_number}'")

    if unit:
        # 处理格式：可能是 "1" 或 "1单元"
        unit_clean = str(unit).strip()
        # 提取数字部分
        unit_match = re.search(r'\d+', unit_clean)
        if unit_match:
            unit_number = unit_match.group()  # 提取数字
            # 搜索数据库中的纯数字或带"单元"的格式
            sales = sales.filter(
                Q(property__unit_number=unit_number) |
                Q(property__unit_number=unit_number + "单元") |
                Q(property__unit_number="单元" + unit_number)
            )
            print(f"DEBUG - 搜索单元: 输入='{unit_clean}', 提取数字='{unit_number}'")

    if floor:
        # 处理格式：可能是 "1" 或 "1层"
        floor_clean = str(floor).strip()
        # 提取数字部分
        floor_match = re.search(r'\d+', floor_clean)
        if floor_match:
            floor_number = int(floor_match.group())  # 提取数字并转为整数
            # 楼层是IntegerField，直接用数字匹配
            sales = sales.filter(property__floor=floor_number)
            print(f"DEBUG - 搜索楼层: 输入='{floor_clean}', 提取数字='{floor_number}'")

    if room:
        # 处理格式：可能是 "101" 或 "101室"
        room_clean = str(room).strip()
        # 提取数字部分
        room_match = re.search(r'\d+', room_clean)
        if room_match:
            room_number = room_match.group()  # 提取数字
            # 搜索数据库中的纯数字或带"室"的格式
            sales = sales.filter(
                Q(property__room_number=room_number) |
                Q(property__room_number=room_number + "室") |
                Q(property__room_number="室" + room_number)
            )
            print(f"DEBUG - 搜索房号: 输入='{room_clean}', 提取数字='{room_number}'")

    # 状态筛选
    if status_filter:
        sales = sales.filter(status=status_filter)

    # 获取当前选中的项目（用于模板中显示静态选项）
    current_project = None
    if selected_project:
        try:
            current_project = Project.objects.get(id=selected_project)
        except Project.DoesNotExist:
            pass

    # 调试信息
    print(f"DEBUG - 搜索参数: project={selected_project}, building={building}, unit={unit}, floor={floor}, room={room}")
    print(f"DEBUG - 查询结果数量: {sales.count()}")

    # 排序和分页
    sales = sales.order_by('-created_at')
    paginator = Paginator(sales, 20)
    page = request.GET.get('page')
    sales_page = paginator.get_page(page)

    context = {
        'sales': sales_page,
        'projects': projects,
        'current_project': current_project,
        'search': search,
        'selected_project': selected_project,
        'building': building,
        'unit': unit,
        'floor': floor,
        'room': room,
        'status': status_filter,
    }

    return render(request, 'sales/sale_list.html', context)

# 其他视图函数保持不变...
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