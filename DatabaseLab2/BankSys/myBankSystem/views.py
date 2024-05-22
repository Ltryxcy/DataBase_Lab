from django.http import HttpResponse
from django.template import loader
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from .models import Bank_Branch, Bank_Department, Bank_Staff, Branch_Manager, Department_Manager
from django.core.paginator import Paginator

# Create your views here.

## 先创建admin的视图
#  支行信息界面的视图
def branches(request):
    branches_lists = Bank_Branch.objects.all() 
    paged = Paginator(branches_lists, 6) # 分页，每页显示6条数据
    branches_page = paged.get_page(request.GET.get('page')) # 获取当前页码
    context = {'branches': branches_page}
    
    managers = Branch_Manager.objects.all() # 获取所有支行负责人
    # 遍历支行信息，将支行负责人添加到支行信息中
    for branch in branches_page:
        for manager in managers:
            if branch.branch_name == manager.branch_name.branch_name:
                branch.manager = manager.staff_name 
    # 返回支行管理界面
    return render(request, 'branches/branches.html', context) 

#  部门信息界面的视图
def departments(request):
    # 获取所有部门信息
    departments_lists = Bank_Department.objects.filter(branch_id = )
    # 分页，每页显示6条数据
    paged = Paginator(departments_lists, 6)
    # 获取当前页码
    departments_page = paged.get_page(request.GET.get('page'))
    
    managers = Department_Manager.objects.all() # 获取所有部门经理
    # 遍历部门信息，将部门经理添加到部门信息中
    for department in departments_page:
        for manager in managers:
            if department.department_id == manager.department.department_id:
                department.manager = manager.staff_name
    context = {'departments': departments_page}
    # 返回部门管理界面
    return render(request, 'departments/departments.html', context)

# 部门员工
def department_staff(request, department_id):
    