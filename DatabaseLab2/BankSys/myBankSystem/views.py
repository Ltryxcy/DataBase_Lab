from django.http import HttpResponse
from django.template import loader
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from .models import Bank_Branch, Bank_Department, Bank_Staff, Branch_Manager, Department_Manager, Bank_Customer,Customer_Account, Transactions, Loan
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, update_session_auth_hash, logout
from .forms import BankCustomer_LoginForm, BankCustomer_RegisterForm, BankCustomer_EditForm, Customer_Accounts_Form, Accounts_Trade_Form
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
        return render(request, 'myBankSystem/error.html', {'error': '没有权限查看'})
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
    customer = User.objects.get(id=user_id)
    # 检查客户是否有未还完的贷款或账户
    loans_exist = Loan.objects.filter(customer_id=user_id).exists()
    accounts_exist = Customer_Account.objects.filter(customer_id=user_id).exists()
    if loans_exist or accounts_exist:
        return render(request, 'myBankSystem/error.html', {'error': '用户名下有未结贷款或账户，无法删除用户'})
    if request.method == 'POST':
        customer.delete()
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
            account = Customer_Account.objects.create(customer=user, branch=branch, money=account_money)
            account.save()
            user.accounts_cnt += 1
            user.save()
            transaction = Transactions.objects.create(account=account, money=account_money, transaction_detail='创建账户')
            transaction.save()
            messages.success(request, '账户创建成功')
            return redirect('myBankSystem:accounts_info', user_id=user.id)
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
    if request.user.id != user_id and not request.user.is_superuser:
        return render(request, 'myBankSystem/error.html', {'error': '无法查看他人账户'})
    # 获取当前用户的账户信息
    account_list = Customer_Account.objects.filter(user_id=account_user.id)
    # 分页，每页显示6条数据
    paged = Paginator(account_list, 6)
    account_page = paged.get_page(request.GET.get('page'))
    context = {'accounts': account_page, 'account_user': account_user}
    return render(request, 'myBankSystem/accounts_info.html', context)

# 删除账户，需要登录状态
@login_required
def delete_account(request, account_id):
    account = Customer_Account.objects.get(account_id=account_id)
    user = Bank_Customer.objects.get(id=account.customer_id)
    # 判断是否为账户的拥有者
    if request.user.id != user.user_id:
        return render(request, 'myBankSystem/error.html', {'error': '无法删除他人账户'})
    if not account or account.money > 0:
        return render(request, 'myBankSystem/error.html', {'error': '无法删除账户'})
    # 触发器，自动更新用户的账户数
    user.accounts_cnt = user.accounts_cnt - 1
    user.save()
    account.delete()
    
    return redirect('myBankSystem:account_info', customer_id=user.id)

# 转账，需要登录状态
@login_required
@transaction.atomic
def trade(request, account_id):
    # 交易方的账户和客户
    account = Customer_Account.objects.get(account_id=account_id)
    customer = Bank_Customer.objects.get(id=account.customer)
    # 判断是否是账户的拥有者
    if request.user.id != customer.id:
        return render(request, 'myBankSystem/error.html', {'error': '您没有此账户权限！'})
    if request.method != 'POST':
        trade_form = Accounts_Trade_Form(initial={'src_account': account})
    else:
        trade_form = Accounts_Trade_Form(initial={'src_account': account}, data=request.POST)
        if trade_form.is_valid():
            money = trade_form.cleaned_data['trade_money']
            target_account = trade_form.cleaned_data['target_account']
            # 判断账户余额是否足够
            if account.money < money:
                return render(request, 'myBankSystem/error.html', {'error': '余额不足'})
            # 目标账户不存在
            if not Customer_Account.objects.filter(account_id=target_account.account_id).exists():
                return render(request, 'myBankSystem/error.html', {'error': '目标账户不存在'})
            # 目标账户不能是自己
            if target_account.account_id == account_id:
                return render(request, 'myBankSystem/error.html', {'error': '不能转账给自己'})
            
            try:
                # 开启事务块
                with transaction.atomic():
                    # 交易方账户扣款
                    account.money = account.money - money
                    account.save()
                    # 目标账户加款
                    target_account.money = target_account.money + money
                    target_account.save()
                    # 生成账单
                    transaction = Transactions.objects.create(account=account, money=money, transaction_detail='转账给'+str(target_account.account_id))
                    transaction.save()
                    transaction = Transactions.objects.create(account=target_account, money=money, transaction_detail='收到'+str(account.account_id)+'转账')
                    transaction.save()
                return redirect('myBankSystem:account_info', customer_id=customer.id)
            except Exception as e:
                # 转账失败
                transaction.rollback()
                return render(request, 'myBankSystem/error.html', {'error': '转账失败'})
            
        context = {'form': trade_form, 'account': account}
        return render(request, 'myBankSystem/trade.html', context)

## 交易记录视图
# 查看交易记录，需要登录状态
@login_required
def transactions_info(request, account_id):
    account = Customer_Account.objects.get(account_id=account_id)
    customer = Bank_Customer.objects.get(id=account.customer_id)
    # 判断是否是账户的拥有者
    if request.user.id != customer.id:
        return render(request, 'myBankSystem/error.html', {'error': '您没有此账户权限！'})
    # 获取账户的交易记录
    transactions_list = Transactions.objects.filter(account_id=account_id)
    # 分页，每页显示6条数据
    paged = Paginator(transactions_list, 6)
    transactions_page = paged.get_page(request.GET.get('page'))
    context = {'transactions': transactions_page, 'account': account}
    return render(request, 'myBankSystem/transactions_info.html', context)

            
        
        