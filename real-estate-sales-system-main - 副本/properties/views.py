from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage  # 添加 PageNotAnInteger 和 EmptyPage
from django.db.models import Q
from .models import Property, PriceHistory, PropertyImage
from .forms import PropertyForm, PriceUpdateForm, PropertyImageForm
from projects.models import Project


def is_manager_or_admin(user):
    """检查用户是否为销售经理或管理员"""
    return user.is_authenticated and (user.is_manager() or user.is_admin())


@login_required
def property_list(request):
    """房源列表 - 所有登录用户可查看"""
    # 获取搜索参数
    search = request.GET.get('search', '')
    project_id = request.GET.get('project', '')
    building = request.GET.get('building', '')
    unit = request.GET.get('unit', '')
    floor = request.GET.get('floor', '')
    room = request.GET.get('room', '')
    status = request.GET.get('status', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')

    # 初始化查询集
    properties = Property.objects.all().select_related('project')

    # 通用搜索框（模糊搜索）
    if search:
        properties = properties.filter(
            Q(project__name__icontains=search) |
            Q(building_number__icontains=search) |
            Q(unit_number__icontains=search) |
            Q(room_number__icontains=search)
        )

    # 项目筛选（精确匹配）
    if project_id:
        properties = properties.filter(project_id=project_id)

    # 楼栋筛选 - 支持多种格式
    if building:
        # 前端可能提交 "5" 或 "5栋"
        # 先尝试精确匹配数字
        building_number = str(building).strip()

        # 构建查询条件：既匹配数字也匹配带"栋"的
        properties = properties.filter(
            Q(building_number=building_number) |  # 匹配 "5"
            Q(building_number=building_number + "栋") |  # 匹配 "5栋"
            Q(building_number="栋" + building_number)  # 匹配 "栋5"（如果有的话）
        )

    # 单元筛选 - 支持多种格式
    if unit:
        unit_number = str(unit).strip()
        properties = properties.filter(
            Q(unit_number=unit_number) |  # 匹配 "1"
            Q(unit_number=unit_number + "单元")  # 匹配 "1单元"
        )

    # 楼层筛选（精确匹配）
    if floor:
        properties = properties.filter(floor=floor)

    # 房号筛选（精确匹配）
    if room:
        properties = properties.filter(room_number=room)

    # 状态筛选（精确匹配）
    if status:
        properties = properties.filter(status=status)

    # 价格范围筛选
    if min_price:
        try:
            min_price = float(min_price)
            properties = properties.filter(total_price__gte=min_price)
        except ValueError:
            pass

    if max_price:
        try:
            max_price = float(max_price)
            properties = properties.filter(total_price__lte=max_price)
        except ValueError:
            pass

    # 分页
    paginator = Paginator(properties, 20)
    page = request.GET.get('page')

    try:
        properties = paginator.page(page)
    except PageNotAnInteger:
        # 如果页码不是整数，显示第一页
        properties = paginator.page(1)
    except EmptyPage:
        # 如果页码超出范围，显示最后一页
        properties = paginator.page(paginator.num_pages)

    projects = Project.objects.all()

    return render(request, 'properties/property_list.html', {
        'properties': properties,
        'projects': projects,
        'search': search,
        'project_id': project_id,
        'building': building,
        'unit': unit,
        'floor': floor,
        'room': room,
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
    images = property_obj.get_images()

    return render(request, 'properties/property_detail.html', {
        'property': property_obj,
        'price_history': price_history,
        'images': images,
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


@login_required
@user_passes_test(is_manager_or_admin)
def property_image_upload(request, pk):
    """上传房源图片 - 仅销售经理和管理员"""
    property_obj = get_object_or_404(Property, pk=pk)

    if request.method == 'POST':
        form = PropertyImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.property = property_obj
            image.save()
            messages.success(request, '图片上传成功')
            return redirect('properties:property_detail', pk=pk)
    else:
        form = PropertyImageForm()

    return render(request, 'properties/image_upload.html', {
        'form': form,
        'property': property_obj,
    })


@login_required
@user_passes_test(is_manager_or_admin)
def property_image_delete(request, pk, image_id):
    """删除房源图片 - 仅销售经理和管理员"""
    property_obj = get_object_or_404(Property, pk=pk)
    image = get_object_or_404(PropertyImage, pk=image_id, property=property_obj)

    if request.method == 'POST':
        image.delete()
        messages.success(request, '图片已删除')
        return redirect('properties:property_detail', pk=pk)

    return render(request, 'properties/image_confirm_delete.html', {
        'property': property_obj,
        'image': image,
    })