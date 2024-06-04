from django.http import HttpResponse
from django.template import loader
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from .models import Bank_Branch, Bank_Department, Bank_Staff, Department_Manager, Bank_Customer,Customer_Account, Transactions, Loan
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, update_session_auth_hash, logout
from .forms import BankCustomer_LoginForm, BankCustomer_RegisterForm, BankCustomer_EditForm, Customer_Accounts_Form, Accounts_Trade_Form, Branch_Creation_Form
from .forms import Staff_Creation_Form, Staff_Edit_Form, Department_Creation_Form, Department_Edit_Form, Branch_Edit_Form, Apply_Loan_Form
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.db import transaction
from django.contrib import messages
import logging
logger = logging.getLogger(__name__)
# Create your views here.

def index(request):
    # 返回主页
    template = loader.get_template('myBankSystem/index.html')
    return HttpResponse(template.render({}, request))


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
                return render(request, 'myBankSystem/error.html', {'error': '用户名或密码错误'})
        else:
            return render(request, 'myBankSystem/error.html', {'error': '不合法输入'})
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
            user.save() # 保存新创建的用户
            bank_customer = Bank_Customer.objects.create(user=user, id=id, name=name, tel=tel, email=email, accounts_cnt=account_cnt)
            bank_customer.save() # 保存新创建的用户
            login(request, user) # 登录
            return redirect('myBankSystem:index')
        else:
            print(creation_form.errors)
            print(bank_customer_registerform.errors)
            return render(request,'myBankSystem/error.html', {'error': '输入不合法或该用户名/身份证号码已注册'})
    else: # 用户访问注册页面
        bank_customer_registerform = BankCustomer_RegisterForm()
        creation_form = UserCreationForm()
        context = {'form': creation_form, 'register_form': bank_customer_registerform}
        # 返回注册页面
        return render(request, 'myBankSystem/register.html', context)


#   用户修改密码视图，需要登录
@login_required
def change_password(request, user_id):
    # 获取用户
    user = User.objects.get(id=user_id)
    # 如果用户不是当前用户
    if user != request.user and not request.user.is_superuser:
        # 返回错误页面，错误信息：没有权限修改密码
        return render(request, 'myBankSystem/error.html', {'error': '没有权限修改密码'})
    if request.method != 'POST':
        form = PasswordChangeForm(user=request.user)
    else:
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            # 更新session，修改完密码后，用户需要重新登录
            update_session_auth_hash(request, form.user)
            logout(request)
            # 返回主页
            return redirect('myBankSystem:index')
    context = {'form': form}
    return render(request, 'myBankSystem/change_password.html', context)

#   用户编辑信息视图
@login_required
def edit_customer(request, user_id):
    # 获取用户
    customer = get_object_or_404(User, id=user_id)
    information = get_object_or_404(Bank_Customer, user_id=user_id)
    # 如果用户不是当前用户，且当前用户不是超级用户，没有权限修改信息
    if customer != request.user and not request.user.is_superuser:
        return render(request, 'myBankSystem/error.html', {'error': '没有权限修改信息'})
    if request.method == 'POST':
        form = BankCustomer_EditForm(instance=information, data=request.POST)
        if form.is_valid():
            information.name = form.cleaned_data['name']
            information.tel = form.cleaned_data['tel']
            information.email = form.cleaned_data['email']
            # form.save()
            information.save()
            # 返回主页
            messages.success(request, '信息已经成功更新')
            return redirect('myBankSystem:index')
        else:
            print(form.errors)
            return render(request, 'myBankSystem/error.html', {'error': '输入不合法'})
    else:
        form = BankCustomer_EditForm(instance=information)
    context = {'form': form, 'user_id': user_id}
    return render(request, 'myBankSystem/edition.html', context)

# 查看用户个人信息
@login_required
def user_info(request, user_id):
    # 获取用户
    user = get_object_or_404(User, id=user_id)
    # 如果用户不是当前用户，且当前用户不是超级用户，没有权限查看信息
    if user != request.user and not request.user.is_superuser:
        return render(request, 'myBankSystem/error.html', {'error': '没有权限查看信息'})
    # 获取用户信息
    customer = Bank_Customer.objects.get(user_id=user_id)
    context = {'customer': customer}
    # 返回用户信息界面
    return render(request, 'myBankSystem/user_info.html', context)

#  获取用户信息，需要管理员权限
@login_required
def fetch_customers_information(request):
    # 检查是否是超级用户
    if request.user.is_superuser:
        # 获取所有用户信息
        customers_lists = Bank_Customer.objects.all()
        # 分页，每页显示6条数据
        paged = Paginator(customers_lists, 6)
        # 获取当前页码
        page_number = request.GET.get('page')
        try:
            customers_page = paged.page(page_number)
        except PageNotAnInteger:
            customers_page = paged.page(1)
        except EmptyPage:
            customers_page = paged.page(paged.num_pages)
        
        context = {'customers': customers_page}
        # 返回用户信息界面
        return render(request, 'myBankSystem/customers_info.html', context)
    else:
        # 返回错误页面，错误信息：没有权限查看
        return render(request, 'myBankSystem/error.html', {'error': '没有权限查看'})

#  TODO:删除用户，需要管理员权限
@login_required
def delete_customer(request, user_id):
    if not request.user.is_superuser:
        return render(request, 'myBankSystem/error.html', {'error': '没有权限删除用户'})
    users = User.objects.get(id=user_id)
    customer = Bank_Customer.objects.get(user_id=user_id)
    # 检查客户是否有未还完的贷款或账户
    loans_exist = Loan.objects.filter(customer_id=user_id).exists()
    accounts_exist = Customer_Account.objects.filter(user_id=customer.id).exists()
    print(f'loans_exist: {loans_exist}, accounts_exist: {accounts_exist}')
    if loans_exist or accounts_exist:
        return render(request, 'myBankSystem/error.html', {'error': '用户名下有未结贷款或账户，无法删除用户'})
    if request.method == 'POST':
        users.delete()
        messages.success(request, '用户已删除')
        return redirect('myBankSystem:customers_info')
    context = {'customer', customer}
    return render(request, 'myBankSystem/confirm_delete.html', context)
    
    
#  退出登录状态
@login_required
def log_out(request):
    # 退出登录
    logout(request)
    # 返回登录页面
    return render(request, 'myBankSystem/logout.html')

# 创建账户，要求处于登录状态
# def create_account(request, user_id):
#     if request.user.is_authenticated:
#         user = get_object_or_404(Bank_Customer, user_id=user_id)
#         if request.user.id != user_id:
#             return render(request, 'myBankSystem/error.html', {'error': '无法为他人创建账户'})
#         if request.method != 'POST':
#             form = Customer_Accounts_Form(initial={'customer': user})
#             form.fields['customer'].queryset = Bank_Customer.objects.filter(user_id=user_id)
#         else:
#             form = Customer_Accounts_Form(request.POST)
#             form.fields['customer'].queryset = Bank_Customer.objects.filter(user_id=user_id)
#             if form.is_valid():
#                 account_money = form.cleaned_data['account_money']
#                 branch = form.cleaned_data['branches']
#                 account = Customer_Account.objects.create(customer=user,branch=branch, money=account_money)
#                 account.save()
#                 # trigger
#                 user.accounts_cnt = user.accounts_cnt + 1
#                 user.save()
#                 transaction = Transactions.objects.create(account=account, money=account_money, transaction_detail='创建账户')
#                 transaction.save()
#                 messages.success(request, '账户创建成功')
#                 return redirect('myBankSystem:accounts_info', user_id=user.id)
#             else:
#                 logger.error("Form is not valid:%s",form.errors)
        
#         context = {'form': form, 'user': user}
#         return render(request, 'myBankSystem/create_account.html', context)
#     else:
#         return redirect('myBankSystem:login')
@login_required
def create_account(request, user_id):
    logger.info(f"User {request.user.id} is trying to create an account for user_id {user_id}")
    user = get_object_or_404(Bank_Customer, user_id=user_id)
    if request.user.id != user_id:
        logger.warning(f"User {request.user.id} tried to create an account for another user {user_id}")
        return render(request, 'myBankSystem/error.html', {'error': '无法为他人创建账户'})

    if request.method == 'POST':
        form = Customer_Accounts_Form(request.POST)
        form.fields['customer'].queryset = Bank_Customer.objects.filter(user_id=user_id)
        if form.is_valid():
            account_money = form.cleaned_data['account_money']
            branch = form.cleaned_data['branches']
            account = Customer_Account.objects.create(user=user, branch=branch, money=account_money)
            account.save()
            user.accounts_cnt += 1
            user.save()
            transaction = Transactions.objects.create(account=account, money=account_money, transaction_type='收入', transaction_detail='创建账户')
            transaction.save()
            messages.success(request, '账户创建成功')
            return redirect('myBankSystem:accounts_info', user_id=user.user_id)
        else:
            logger.error("Form is not valid: %s", form.errors)
    else:
        form = Customer_Accounts_Form(initial={'customer': user})
        form.fields['customer'].queryset = Bank_Customer.objects.filter(user_id=user_id)
    
    context = {'form': form, 'user': user}
    return render(request, 'myBankSystem/create_account.html', context)


#  显示当前客户名下的账户信息，需要登录状态
@login_required
def accounts_info(request, user_id):
    print(f'user_id: {user_id}')
    account_user = get_object_or_404(Bank_Customer, user_id=user_id)
    print(f'account_user.id: {account_user.id}')
    if request.user.id != user_id and not request.user.is_superuser:
        return render(request, 'myBankSystem/error.html', {'error': '无法查看他人账户'})
    # 获取当前用户的账户信息
    account_list = Customer_Account.objects.filter(user_id=account_user.id)
    print(f'account_list: {account_list.count()}')
    # 分页，每页显示3条数据
    paged = Paginator(account_list, 3)
    print(f'paged: {paged}')
    account_page = paged.get_page(request.GET.get('page'))
    context = {'accounts': account_page, 'account_user': account_user}
    return render(request, 'myBankSystem/accounts_info.html', context)


# 删除账户，需要登录状态
@login_required
def delete_account(request, account_id):
    # 获取当前账户
    account = Customer_Account.objects.get(account_id=account_id)
    #  获取账户的拥有者
    user = Bank_Customer.objects.get(user_id=account.user.user_id)
    # 判断是否为账户的拥有者
    if request.user.id != user.user_id:
        return render(request, 'myBankSystem/error.html', {'error': '无法删除他人账户'})
    if not account or account.money > 0:
        return render(request, 'myBankSystem/error.html', {'error': '无法删除账户'})
    # 触发器，自动更新用户的账户数
    user.accounts_cnt = user.accounts_cnt - 1
    user.save()
    account.delete()
    
    return redirect('myBankSystem:accounts_info', user_id=user.user_id)

# 转账，需要登录状态
@login_required
@transaction.atomic
def trade(request, account_id):
    try:
        account = Customer_Account.objects.get(account_id=account_id)
        customer = account.user

        # 判断是否是账户的拥有者
        if request.user != customer.user:
            return render(request, 'myBankSystem/error.html', {'error': '您没有此账户权限！'})

        if request.method == 'POST':
            trade_form = Accounts_Trade_Form(request.POST, initial={'src_account': account})
            if trade_form.is_valid():
                money = trade_form.cleaned_data['trade_money']
                target_account = trade_form.cleaned_data['target_account']

                # 判断账户余额是否足够
                if account.money < money:
                    print(f'账户余额: {account.money}, 转账金额: {money}')
                    return render(request, 'myBankSystem/error.html', {'error': '余额不足'})

                # 目标账户不能是自己
                if target_account.account_id == account_id:
                    return render(request, 'myBankSystem/error.html', {'error': '不能转账给自己'})

                # 开启事务块
                with transaction.atomic():
                    # 交易方账户扣款
                    account.money -= money
                    account.save()

                    # 目标账户加款
                    target_account.money += money
                    target_account.save()

                    # 生成账单
                    Transactions.objects.create(account=account, money=-money, transaction_detail=f'转账给 {target_account.account_id}')
                    Transactions.objects.create(account=target_account, money=money,transaction_type='收入', transaction_detail=f'收到 {account.account_id} 转账')

                return redirect('myBankSystem:accounts_info', user_id = customer.user_id)
            else:
                context = {'form': trade_form, 'account': account}
                return render(request, 'myBankSystem/trade.html', context)
        else:
            trade_form = Accounts_Trade_Form(initial={'src_account': account})
            context = {'form': trade_form, 'account': account}
            return render(request, 'myBankSystem/trade.html', context)
    except Customer_Account.DoesNotExist:
        return render(request, 'myBankSystem/error.html', {'error': '账户不存在'})
    except Exception as e:
        return render(request, 'myBankSystem/error.html', {'error': f'转账失败: {str(e)}'})

# 转入金额，需要登录状态



## 交易记录视图
# 查看交易记录，需要登录状态
@login_required
def transactions_info(request, account_id):
    account = Customer_Account.objects.get(account_id=account_id)
    customer = Bank_Customer.objects.get(id=account.user.id)
    # 判断是否是账户的拥有者
    if request.user.id != customer.user_id:
        return render(request, 'myBankSystem/error.html', {'error': '您没有此账户权限！'})
    # 获取账户的交易记录
    transactions_list = Transactions.objects.filter(account_id=account_id).order_by('transaction_id')
    # 分页，每页显示6条数据
    paged = Paginator(transactions_list, 6)
    transactions_page = paged.get_page(request.GET.get('page'))
    context = {'transactions': transactions_page, 'account': account}
    return render(request, 'myBankSystem/transactions_info.html', context)
   

    
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
            if department.department_id == manager.departments.department_id:
                department.department_manager = manager.staffs.staff_name
    context = {'departments': departments_page}
    # 返回部门管理界面
    template = loader.get_template('myBankSystem/departments.html')
    return HttpResponse(template.render(context, request))

# 创建部门，需要登录状态，管理员权限
@login_required
def create_department(request):
    if not request.user.is_superuser:
        return render(request, 'myBankSystem/error.html', {'error': '没有权限创建部门'})
    
    # branch = Bank_Branch.objects.
    
    if request.method != 'POST':
        form = Department_Creation_Form()
    else:
        form = Department_Creation_Form(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('myBankSystem:departments')
        else:
            logger.error(f"Form is not valid: {form.errors}")
    
    context = {'form': form}
    return render(request, 'myBankSystem/create_department.html', context)

# 修改部门信息，需要登录状态，管理员权限
@login_required
def edit_department(request, department_id):
    if not request.user.is_superuser:
        return render(request, 'myBankSystem/error.html', {'error': '没有权限编辑部门信息'})
    department = Bank_Department.objects.get(department_id=department_id)
    if request.method != 'POST':
        form = Department_Edit_Form(instance=department)
    else:
        form = Department_Edit_Form(instance=department, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('myBankSystem:departments')
        else:
            logger.error(f"Form is not valid: {form.errors}")
    context = {'form': form, 'department': department}
    return render(request, 'myBankSystem/edit_department.html', context)

# 删除部门，需要登录状态，管理员权限
@login_required
def delete_department(request, department_id):
    if not request.user.is_superuser:
        return render(request, 'myBankSystem/error.html', {'error': '没有权限删除部门'})
    department = Bank_Department.objects.get(department_id=department_id)
    # 如果部门有员工，不能删除
    if Bank_Staff.objects.filter(department_id=department_id).exists():
        return render(request, 'myBankSystem/error.html', {'error': '部门下有员工，无法删除部门'})
    # 删除部门
    department.delete()
    return redirect('myBankSystem:departments')

##  部门员工的视图
def department_staff(request, department_id):
    if not request.user.is_superuser:
        return render(request, 'myBankSystem/error.html', {'error': '没有权限查看部门员工'})
    staff_lists = Bank_Staff.objects.filter(department_id=department_id) # 获取部门员工信息
    # 分页，每页显示6条数据
    paged = Paginator(staff_lists, 6)
    # 获取当前页码
    staff_page = paged.get_page(request.GET.get('page'))
    context = {'staffs': staff_page}
    return render(request, 'myBankSystem/department_staff.html', context)

@login_required
def create_staff(request, department_id):
    #  判断是否是超级用户
    if not request.user.is_superuser:
        return render(request, 'myBankSystem/error.html', {'error': '没有权限创建员工'})
    # 获取部门和支行信息
    branch = Bank_Department.objects.get(department_id=department_id).branch.branch_name
    department = Bank_Department.objects.get(department_id=department_id)
    if request.method != 'POST':
        form = Staff_Creation_Form(initial={'department': department})
    # 处理表单提交
    else:
        form = Staff_Creation_Form(initial={'department':department},data=request.POST,files=request.FILES)
        # 判断表单是否合法
        if form.is_valid():
            name = form.cleaned_data['name']
            tel = form.cleaned_data['tel']
            sex = form.cleaned_data['sex']
            staff = Bank_Staff.objects.create(department=department, staff_name=name, staff_tel=tel, staff_sex=sex)
            if 'photo' in request.FILES:
                staff.staff_photo = form.cleaned_data['photo']
            staff.save()
            return redirect('myBankSystem:department_staff', department_id=department_id)
        else:
            print(f'form.errors: {form.errors}')
    context = {'form': form, 'department': department}
    return render(request, 'myBankSystem/create_staff.html', context)

# 员工信息展示
@login_required
def staff_list(request):
    if not request.user.is_superuser:
        return render(request, 'myBankSystem/error.html', {'error': '没有权限查看员工信息'})
    staff_list = Bank_Staff.objects.all()
    paginator = Paginator(staff_list, 6)  # 每页显示6个员工
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'myBankSystem/department_staff.html', context)

# 删除员工，需要登录状态，管理员权限
@login_required
def delete_staff(request, staff_id):
    # 查看是否有权限
    if not request.user.is_superuser:
        return render(request, 'myBankSystem/error.html', {'error': '没有权限删除员工'})
    # 找到对应员工
    staff = Bank_Staff.objects.get(staff_id=staff_id)
    department = staff.department
    # 删除员工，考虑是否是部门经理
    if Department_Manager.objects.filter(staff_id=staff_id):
        manager = Department_Manager.objects.get(staff_id=staff_id)
        manager.delete()
    # 删除员工照片
    if staff.staff_photo.name != 'default.jpg':
        staff.staff_photo.delete()
    staff.delete()
    return redirect('myBankSystem:department_staff', department_id=department.department_id)

# 编辑员工信息，需要登录状态，管理员权限
@login_required
def edit_staff(request, staff_id):
    if not request.user.is_superuser:
        return render(request, 'myBankSystem/error.html', {'error': '没有权限编辑员工信息'})
    staff = Bank_Staff.objects.get(staff_id=staff_id)
    pre_department = staff.department
    if request.method != 'POST':
        form = Staff_Edit_Form(instance=staff)
    else:
        form = Staff_Edit_Form(instance=staff, data=request.POST, files=request.FILES)
        if form.is_valid():
            staff.department = form.cleaned_data['department']
            staff.staff_name = form.cleaned_data['name']
            staff.staff_tel = form.cleaned_data['tel']
            staff.staff_sex = form.cleaned_data['sex']
            # 如果是部门经理并且更换了部门，删除原部门经理
            if pre_department != staff.department and Department_Manager.objects.filter(departments_id=pre_department.department_id):
                manager = Department_Manager.objects.get(departments_id=pre_department.department_id)
                manager.delete()
            if 'photo' in request.FILES:
                # 删除旧照片
                if staff.staff_photo.name != 'photos/default.jpg':
                    staff.staff_photo.delete()
                staff.staff_photo = form.cleaned_data['photo']
            staff.save()
            return redirect('myBankSystem:department_staff', department_id=staff.department.department_id)
        else:
            logger.error(f"Form is not valid: {form.errors}")
    context = {'form': form, 'staff': staff}
    return render(request, 'myBankSystem/edit_staff.html', context)

# 设置部门经理，需要登录状态，管理员权限
@login_required
def set_manager(request, staff_id, department_id):
    if not request.user.is_superuser:
        return render(request, 'myBankSystem/error.html', {'error': '没有权限设置部门经理'})

    try:
        staff = Bank_Staff.objects.get(staff_id=staff_id)
    except Bank_Staff.DoesNotExist:
        return render(request, 'myBankSystem/error.html', {'error': '找不到指定员工'})

    department = get_object_or_404(Bank_Department, department_id=department_id)

    # 如果已经有部门经理，报错，请先删除原经理
    if Department_Manager.objects.filter(departments=department).exists():
        return render(request, 'myBankSystem/error.html', {'error': '部门已有经理，请先删除原经理'})

    # 创建部门经理，显式指定 department_id 字段
    manager = Department_Manager(departments=department, staffs=staff)
    manager.save()

    return redirect('myBankSystem:departments')


# 删除部门经理，需要登录状态，管理员权限
@login_required
def delete_manager(request, department_id):
    if not request.user.is_superuser:
        return render(request, 'myBankSystem/error.html', {'error': '没有权限删除部门经理'})
    department = Bank_Department.objects.get(department_id=department_id)
    # 获取部门经理
    manager = Department_Manager.objects.get(departments=department)
    if manager:
        manager.delete()
    return redirect('myBankSystem:departments')



##  支行信息界面的视图
def branches(request):
    # 获取所有支行信息并按支行名称排序
    branches_lists = Bank_Branch.objects.all().order_by('branch_name') 
    paged = Paginator(branches_lists, 6) # 分页，每页显示6条数据
    branches_page = paged.get_page(request.GET.get('page')) # 获取当前页码
    context = {'branches': branches_page}
    
    # 返回支行管理界面
    template = loader.get_template('myBankSystem/branches.html')
    return HttpResponse(template.render(context, request))

# 创建支行，需要登录状态，管理员权限
@login_required
def create_branch(request):
    if not request.user.is_superuser:
        return render(request, 'myBankSystem/error.html', {'error': '没有权限创建支行'})
    if request.method == 'POST':
        form = Branch_Creation_Form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('myBankSystem:branches')  # 假设有一个显示支行列表的视图
    else:
        form = Branch_Creation_Form()
    
    return render(request, 'myBankSystem/create_branch.html', {'form': form})

# 删除支行，需要登录状态，管理员权限
@login_required
def delete_branch(request, branch_name):
    if not request.user.is_superuser:
        return render(request, 'myBankSystem/error.html', {'error': '没有权限删除支行'})
    branch = Bank_Branch.objects.get(branch_name=branch_name)
    if Bank_Department.objects.filter(branch=branch_name).exists():
        return render(request, 'myBankSystem/error.html', {'error': '支行下有部门，无法删除'})
    branch.delete()
    return redirect('myBankSystem:branches')

# 修改支行信息，需要登录状态，管理员权限
def edit_branch(request, branch_name):
    if not request.user.is_superuser:
        return render(request, 'myBankSystem/error.html', {'error': '没有权限编辑支行信息'})
    branch = Bank_Branch.objects.get(branch_name=branch_name)
    if request.method != 'POST':
        form = Branch_Edit_Form(instance=branch)
    else:
        post_data = request.POST.copy()
        post_data['branch_name'] = branch_name
        form = Branch_Edit_Form(instance=branch, data=post_data)
        if form.is_valid():
            form.save()
            return redirect('myBankSystem:branches')
        else:
            logger.error(f"Form is not valid: {form.errors}")
    context = {'form': form, 'branch': branch}
    return render(request, 'myBankSystem/edit_branch.html', context)

# 贷款信息界面的视图
# 申请贷款，需要登录状态
@login_required
def apply_loan(request, user_id, branch_name):
    user = get_object_or_404(Bank_Customer, user_id=user_id)
    if request.user.id != user_id:
        return render(request, 'myBankSystem/error.html', {'error': '无法为他人申请贷款'})
    branch = get_object_or_404(Bank_Branch, branch_name=branch_name)
    if request.method != 'POST':
        form = Apply_Loan_Form(initial={'user': user, 'branch': branch})
    else:
        form = Apply_Loan_Form(initial={'user': user, 'branch': branch}, data=request.POST)
        if form.is_valid():
            money = form.cleaned_data['money']
            loan = Loan.objects.create(customer=user, branch=branch, loan_total=money, loan_balance=money)
            loan.save()
            return redirect('myBankSystem:index')
    context = {'form': form}
    return render(request, 'myBankSystem/apply_loan.html', context)
# 查询用户名下的贷款信息，需要登录状态
@login_required
def loans_info(request, user_id):
    user = get_object_or_404(Bank_Customer, user_id=user_id)
    if request.user.id != user_id:
        return render(request, 'myBankSystem/error.html', {'error': '无法查看他人贷款信息'})
    loans_list = Loan.objects.filter(customer=user)
    # 分页，每页显示6条数据
    paged = Paginator(loans_list, 6)
    loans_page = paged.get_page(request.GET.get('page'))
    context = {'loans': loans_page, 'user': user}
    return render(request, 'myBankSystem/loans_info.html', context)


