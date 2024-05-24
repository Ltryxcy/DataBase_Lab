from django.http import HttpResponse
from django.template import loader
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from .models import Bank_Branch, Bank_Department, Bank_Staff, Branch_Manager, Department_Manager
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.template import loader
from django.contrib.auth import authenticate, login
from .forms 

# Create your views here.



##  支行信息界面的视图
def branches(request):
    # 获取所有支行信息并按支行名称排序
    branches_lists = Bank_Branch.objects.all().order_by('branch_name') 
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
    template = loader.get_template('myBankSystem/branches.html')
    return HttpResponse(template.render(context, request))
    
##  部门信息界面的视图
def departments(request):
    # 获取所有部门信息
    departments_lists = Bank_Department.objects.all()
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
    template = loader.get_template('myBankSystem/departments.html')
    return HttpResponse(template.render(context, request))

##  部门员工的视图
def department_staff(request, department_id):
    branch_name = None
    if request.user.is_superuser:
        branch_name = request.user.username
    # 获取部门所属支行名称
    branch = Bank_Department.objects.get(department_id=department_id).branch.branch_name
    # 如果当前用户不是超级用户或者当前用户不是部门所属支行的支行负责人
    if (branch_name == None) or (branch_name != branch):
        # 返回错误页面，错误信息：没有权限查看
        return render(request, 'error.html', {'error': '没有权限查看'})
    staff_lists = Bank_Staff.objects.filter(department_id=department_id) # 获取部门员工信息
    # 分页，每页显示6条数据
    paged = Paginator(staff_lists, 6)
    # 获取当前页码
    staff_page = paged.get_page(request.GET.get('page'))
    context = {'staffs': staff_page}
    return render(request, 'myBankSystem/department_staff.html', context)

##  用户登录界面
def bank_user_login(request):
    if request.method == 'POST': # 用户提交登录信息
        
    
