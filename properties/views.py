from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Property, PriceHistory
from .forms import PropertyForm, PriceUpdateForm
from projects.models import Project


def is_manager_or_admin(user):
    """检查用户是否为销售经理或管理员"""
    return user.is_authenticated and (user.is_manager() or user.is_admin())


@login_required
def property_list(request):
    """房源列表 - 所有登录用户可查看"""
    properties = Property.objects.all()
    
    # 搜索功能
    search = request.GET.get('search', '')
    if search:
        properties = properties.filter(
            Q(project__name__icontains=search) |
            Q(building_number__icontains=search) |
            Q(room_number__icontains=search)
        )
    
    # 项目筛选
    project_id = request.GET.get('project', '')
    if project_id:
        properties = properties.filter(project_id=project_id)
    
    # 状态筛选
    status = request.GET.get('status', '')
    if status:
        properties = properties.filter(status=status)
    
    # 价格范围筛选
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    if min_price:
        properties = properties.filter(total_price__gte=min_price)
    if max_price:
        properties = properties.filter(total_price__lte=max_price)
    
    paginator = Paginator(properties, 20)
    page = request.GET.get('page')
    properties = paginator.get_page(page)
    
    projects = Project.objects.all()
    
    return render(request, 'properties/property_list.html', {
        'properties': properties,
        'projects': projects,
        'search': search,
        'project_id': project_id,
        'status': status,
        'min_price': min_price,
        'max_price': max_price,
    })


@login_required
@user_passes_test(is_manager_or_admin)
def property_create(request):
    """创建房源 - 仅销售经理和管理员"""
    if request.method == 'POST':
        form = PropertyForm(request.POST)
        if form.is_valid():
            property_obj = form.save(commit=False)
            property_obj.created_by = request.user
            property_obj.save()
            messages.success(request, f'房源创建成功')
            return redirect('properties:property_list')
    else:
        form = PropertyForm()
    
    return render(request, 'properties/property_form.html', {
        'form': form,
        'title': '创建房源',
    })


@login_required
@user_passes_test(is_manager_or_admin)
def property_update(request, pk):
    """更新房源 - 仅销售经理和管理员"""
    property_obj = get_object_or_404(Property, pk=pk)
    
    if request.method == 'POST':
        form = PropertyForm(request.POST, instance=property_obj)
        if form.is_valid():
            form.save()
            messages.success(request, f'房源更新成功')
            return redirect('properties:property_list')
    else:
        form = PropertyForm(instance=property_obj)
    
    return render(request, 'properties/property_form.html', {
        'form': form,
        'title': '更新房源',
        'property': property_obj,
    })


@login_required
def property_detail(request, pk):
    """房源详情"""
    property_obj = get_object_or_404(Property, pk=pk)
    price_history = PriceHistory.objects.filter(property=property_obj)[:10]
    
    return render(request, 'properties/property_detail.html', {
        'property': property_obj,
        'price_history': price_history,
    })


@login_required
@user_passes_test(is_manager_or_admin)
def property_delete(request, pk):
    """删除房源"""
    property_obj = get_object_or_404(Property, pk=pk)
    if request.method == 'POST':
        property_obj.delete()
        messages.success(request, '房源已删除')
        return redirect('properties:property_list')
    
    return render(request, 'properties/property_confirm_delete.html', {'property': property_obj})


@login_required
@user_passes_test(is_manager_or_admin)
def price_update(request, pk):
    """更新价格 - 仅销售经理和管理员"""
    property_obj = get_object_or_404(Property, pk=pk)
    
    if request.method == 'POST':
        form = PriceUpdateForm(request.POST, instance=property_obj)
        if form.is_valid():
            # 保存旧价格到历史记录
            old_unit_price = property_obj.unit_price
            old_total_price = property_obj.total_price
            
            # 更新价格
            property_obj.unit_price = form.cleaned_data['unit_price']
            property_obj.total_price = form.cleaned_data['total_price']
            property_obj.save()
            
            # 如果价格有变化，记录到历史
            if old_unit_price != property_obj.unit_price or old_total_price != property_obj.total_price:
                PriceHistory.objects.create(
                    property=property_obj,
                    unit_price=property_obj.unit_price,
                    total_price=property_obj.total_price,
                    changed_by=request.user,
                    reason=form.cleaned_data.get('reason', '')
                )
            
            messages.success(request, '价格更新成功')
            return redirect('properties:property_detail', pk=pk)
    else:
        form = PriceUpdateForm(instance=property_obj)
    
    return render(request, 'properties/price_form.html', {
        'form': form,
        'property': property_obj,
    })

