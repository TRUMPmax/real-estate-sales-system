from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Project
from .forms import ProjectForm


def is_manager_or_admin(user):
    """检查用户是否为销售经理或管理员"""
    return user.is_authenticated and (user.is_manager() or user.is_admin())


@login_required
@user_passes_test(is_manager_or_admin)
def project_list(request):
    """项目列表"""
    projects = Project.objects.all()
    
    search = request.GET.get('search', '')
    if search:
        projects = projects.filter(name__icontains=search) | projects.filter(address__icontains=search)
    
    paginator = Paginator(projects, 20)
    page = request.GET.get('page')
    projects = paginator.get_page(page)
    
    return render(request, 'projects/project_list.html', {
        'projects': projects,
        'search': search,
    })


@login_required
@user_passes_test(is_manager_or_admin)
def project_create(request):
    """创建项目"""
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            project.save()
            messages.success(request, f'项目 {project.name} 创建成功')
            return redirect('projects:project_list')
    else:
        form = ProjectForm()
    
    return render(request, 'projects/project_form.html', {
        'form': form,
        'title': '创建项目',
    })


@login_required
@user_passes_test(is_manager_or_admin)
def project_update(request, pk):
    """更新项目"""
    project = get_object_or_404(Project, pk=pk)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, f'项目 {project.name} 更新成功')
            return redirect('projects:project_list')
    else:
        form = ProjectForm(instance=project)
    
    return render(request, 'projects/project_form.html', {
        'form': form,
        'title': '更新项目',
        'project': project,
    })


@login_required
@user_passes_test(is_manager_or_admin)
def project_detail(request, pk):
    """项目详情"""
    project = get_object_or_404(Project, pk=pk)
    from properties.models import Property
    properties = Property.objects.filter(project=project)
    
    return render(request, 'projects/project_detail.html', {
        'project': project,
        'properties': properties,
    })


@login_required
@user_passes_test(is_manager_or_admin)
def project_delete(request, pk):
    """删除项目"""
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        name = project.name
        project.delete()
        messages.success(request, f'项目 {name} 已删除')
        return redirect('projects:project_list')
    
    return render(request, 'projects/project_confirm_delete.html', {'project': project})

