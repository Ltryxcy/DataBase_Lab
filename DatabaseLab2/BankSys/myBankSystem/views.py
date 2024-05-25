from django.http import HttpResponse
from django.template import loader
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from .models import Bank_Branch, Bank_Department, Bank_Staff, Branch_Manager, Department_Manager, Bank_Customer,Customer_Account
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.template import loader
from django.contrib.auth import authenticate, login
from .forms import BankCustomer_LoginForm, BankCustomer_RegisterForm, BankCustomer_EditForm
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

def index(request):
    # 返回主页
    return render(request, 'myBankSystem/index.html')

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
def bank_customer_login(request):
    if request.method == 'POST': # 用户提交登录信息
        bank_customer_loginform = BankCustomer_LoginForm(request.POST)
        # 判断登录表单是否有效
        if bank_customer_loginform.is_valid():
            # 获取用户名和密码
            user_name = bank_customer_loginform.cleaned_data['username']
            password = bank_customer_loginform.cleaned_data['password']
            # 认证
            user = authenticate(username=user_name, password=password)
            # 如果用户存在
            if user is not None:
                # 登录
                login(request, user)
                # 返回主页
                return redirect('myBankSystem:index')
            else:
                # 返回错误页面，错误信息：用户名或密码错误
                return render(request, 'error.html', {'error': '用户名或密码错误'})
        else:
            return render(request, 'error.html', {'error': '不合法输入'})
    elif request.method == 'GET': # 用户访问登录页面
        bank_customer_loginform = BankCustomer_LoginForm()
        context = {'form': bank_customer_loginform}
        # 返回登录页面
        return render(request, 'myBankSystem/login.html', context) 
#   用户注册界面
def bank_customer_register(request):
    if request.method == 'POST':
        bank_customer_registerform = BankCustomer_RegisterForm(request.POST)
        # 处理用户注册，进行初始化
        creation_form = UserCreationForm(request.POST)
        if creation_form.is_valid() and bank_customer_registerform.is_valid():
            user_name = creation_form.cleaned_data['username']
            password = creation_form.cleaned_data['password1']
            id = bank_customer_registerform.cleaned_data['id']
            name = bank_customer_registerform.cleaned_data['name']
            tel = bank_customer_registerform.cleaned_data['tel']
            email = bank_customer_registerform.cleaned_data['email']
            account_cnt = bank_customer_registerform.cleaned_data['account_cnt']
            # 创建用户
            user = User.objects.create_user(username=user_name, password=password)
            bank_customer = Bank_Customer.objects.create(user=user, id=id, name=name, tel=tel, email=email, account_cnt=account_cnt)
            bank_customer.save() # 保存新创建的用户
            login(request, user) # 登录
            return redirect('myBankSystem:index')
        else:
            return render(request, 'error.html', {'error': '输入不合法或该用户名/身份证号码已注册'})
    elif request.method == 'GET': # 用户访问注册页面
        bank_customer_registerform = BankCustomer_RegisterForm()
        creation_form = UserCreationForm()
        context = {'form': creation_form, 'register_form': bank_customer_registerform}
        # 返回注册页面
        return render(request, 'myBankSystem/register.html', context)
        
    