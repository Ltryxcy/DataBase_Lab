<div style="text-align:center;font-size:2em;font-weight:bold">中国科学技术大学计算机学院</div>



<div style="text-align:center;font-size:2em;font-weight:bold">《数据库系统实验报告》</div>







<img src="./src/logo.png" style="zoom: 50%;" />





<div style="display: flex;flex-direction: column;align-items: center;font-size:2em">
<div>
<p>实验题目：银行管理系统</p>
<p>学生姓名：刘川毅</p>
<p>学生学号：PB21111718</p>
<p>完成时间：2024年6月4日</p>
</div>
</div>

<div style="page-break-after:always"></div>

## 需求分析

### 数据需求分析

一个银行会下辖多个支行，每个支行可以用支行名称唯一确定，同时还要记录支行的地址、联系电话和负责人，支行负责人和支行之间也是一对一关系。每个支行会有多个部门，部门可由部门号唯一决定，同时需要记录部门名称、部门所属银行和部门经理，部门经理和部门是一对一关系。部门下有多个员工，员工可以通过工号唯一决定（可能存在重名员工），同时还要记录员工的姓名，性别，身份证号，手机号，家庭住址，员工中。银行中有若干客户，客户可以由客户的身份证号唯一决定，同时记录客户的姓名，名下的账户数量，手机号和邮箱。然后管理账户，每个账户由账户号唯一决定，账户中记录账户的余额和密码。每个账户的转账历史都被存储在交易记录中，交易记录由交易记录号唯一标识，其中记录了账户号，修改的账户净值，交易类型（收入/支出），交易详情和时间。最后，作为银行，还需要管理贷款，每笔贷款由贷款号唯一标识，需要记录贷款人，借贷总额，借贷日期，还款期限和未还清余额。下面根据数据需求分析进行初步的实体需求设计：

### 实体需求设计

初步考虑下，得到的实体以及对应的属性设计如下：

- 银行支行：<u>支行名称</u>，支行地址，联系电话，支行负责人
- 部门：<u>部门号</u>，部门名称，部门负责人
- 员工：<u>工号</u>，姓名，性别，手机号，照片
- 客户：<u>身份证号</u>，姓名，名下账户数量，手机号，邮箱
- 账户：<u>账户号</u>，账户余额，开户时间
- 交易记录：<u>交易记录号</u>， 修改净值，交易类型，交易详情，交易时间
- 贷款：<u>贷款号</u>，借贷总额，借贷日期，还款期限，未还清余额

### 功能需求

- 银行信息管理：提供支行信息查询和修改功能，提供新增/删除支行的功能，支行信息均不能为空。需要支持地址和联系电话的修改，只有管理员才能删除支行，并且要满足支行内的账户为空且支行中没有未还完的贷款。
- 客户信息管理：提供新增、删除客户的功能，删除客户需要满足客户名下账户数量为0并且没有贷款。提供查询和修改客户信息的功能。提供在网页端的客户注册、登录和退出登录。
- 账户信息管理：允许新增账户和删除账户，删除账户要满足账户中没有余额的条件。支持修改和查询账户信息，账户内存钱取钱，账户间转账等功能。
- 银行部门信息管理：提供银行部门的增加、删除功能。提供修改和查询部门信息的功能，不能修改部门号，还可以修改部门经理。
- 员工信息管理：提供员工信息的增加、删除、修改和查询功能，在这里实现图像文件的管理。

- 贷款信息管理：提供贷款信息的查询、增加、修改功能，未归还清的贷款记录不能删除，贷款记录的删除类似触发器，当贷款未还金额为0时自动删除贷款。
- 交易记录管理：提供交易记录的查询功能，不能删除已有的交易记录，可以通过手动增加交易记录的方式实现账户存取钱的功能，账户间的交易会自动添加交易记录。

## 总体设计

### 系统模块结构

本次实验采用了 B/S 架构，通过 Python + Django 实现。前端部分主要是编写HTML模板渲染网页，后端部分采用了 MySQL 作为数据库平台，通过 Django 提供的模型层、视图层在数据库中创建表，处理用户请求并返回响应。

### 数据库设计

将上述的实体、实体属性和联系转换为ER模型并绘制ER图，如下：

![image-20240604210729713](C:\Users\86134\AppData\Roaming\Typora\typora-user-images\image-20240604210729713.png)

其中，有下划线的属性是实体的标识，部门经理是员工的一个子类。

## 数据库逻辑设计

### 基本ER模型转换到关系模型

> 先将每个实体转换为一个关系模式，实体的属性为关系模式的属性，实体的标识为关系模式的主码：

- 银行支行（<u>支行名称</u>，所在城市，联系电话）
- 银行部门（<u>部门号</u>，部门名称，部门经理）
- 员工（<u>工号</u>，员工照片，姓名，性别，手机号）
- 客户（<u>身份证号</u>，姓名，手机号，邮箱，名下账户数）
- 账户（<u>账户号</u>，账户余额，开户时间）
- 交易记录（<u>交易记录号</u>，修改净值，交易类型，交易详情）
- 贷款（<u>贷款号</u>，还款期限，未还清余额）

> 然后进行联系转换，1 : 1 联系中，将任一端的实体标识和联系属性加入另一实体所对应的关系模式中，两个模式的主码保持不变；1 : N 联系中，将 1 端实体的标识和联系属性加入到 N 端实体对应的关系模式中。

- 银行支行（<u>支行名称</u>，所在城市，联系电话）
- 银行部门（<u>部门号</u>，支行名称，部门名称，部门经理）
- 员工（<u>工号</u>，员工照片，姓名，性别，手机号，部门号）
- 客户（<u>身份证号</u>，姓名，手机号，邮箱，名下账户数）
- 账户（<u>账户号</u>，账户余额，开户时间，身份证号，支行名称）
- 交易记录（<u>交易记录号</u>，修改净值，交易类型，交易详情，账户号，交易时间）
- 贷款（<u>贷款号</u>，贷款总额，还款期限，未还清余额，身份证号，支行名称，贷款日期）

### 扩展ER模型转换到关系模型

> 由于ER图中没有弱实体，所以不用考虑弱实体转换，只用考虑子类转换。将父类和子类实体都各自转换为关系模式，并将父类的主码加入子类关系模式中并设为主码。因为前面联系转换的时候没有考虑子类，所以同时要考虑子类的联系转换，将部门的标识加入到部门经理的关系模式中。得到初步的关系数据库模式如下：

- 银行支行（<u>支行名称</u>，所在城市，联系电话）
- 银行部门（<u>部门号</u>，支行名称，部门名称，部门经理）
- 员工（<u>工号</u>，员工照片，姓名，性别，手机号，部门号）
- 部门经理（<u>工号</u>，部门号）
- 客户（<u>身份证号</u>，姓名，手机号，邮箱，名下账户数）
- 账户（<u>账户号</u>，账户余额，开户时间，身份证号，支行名称）
- 交易记录（<u>交易记录号</u>，修改净值，交易类型，交易详情，账户号，交易时间）
- 贷款（<u>贷款号</u>，贷款总额，还款期限，未还清余额，身份证号，支行名称，贷款日期）

### 关系数据库模式规范化

> 下面要确定范式级别并实施规范化处理，先列出所有的函数依赖集，如下：

$FD_{银行支行}=\{支行名称\rightarrow 所在城市，支行名称\rightarrow 所在城市支行负责人\}$

$FD_{银行部门}=\{部门号\rightarrow 支行名称，部门号\rightarrow 部门名称，部门号\rightarrow 部门经理 \}$

$FD_{员工}=\{工号\rightarrow员工照片，工号\rightarrow姓名，工号\rightarrow性别，工号\rightarrow手机号，工号\rightarrow部门号 \}$

$FD_{客户}=\{ 身份证号\rightarrow姓名，身份证号\rightarrow 手机号，身份证号\rightarrow邮箱，身份证号\rightarrow名下账户数 \}$

$FD_{账户}=\{账户号\rightarrow账户余额，账户号\rightarrow开户时间，账户号\rightarrow 身份证号，账户号\rightarrow支行名称 \}$

$FD_{交易记录}=\{交易记录号\rightarrow修改净值，交易记录号\rightarrow交易类型，交易记录号\rightarrow交易详情，交易记录号\rightarrow账户号，交易记录号\rightarrow交易时间  \}$

$FD_{贷款}=\{贷款号\rightarrow贷款总额，贷款号\rightarrow还款期限，贷款号\rightarrow未清还余额，贷款号\rightarrow身份证号，贷款号\rightarrow支行名称，贷款号\rightarrow贷款日期  \}$

> 通过各关系模式的函数依赖集可以看出，每个函数依赖集都已经是最小函数依赖集，并且通过规范化分析，前面得出的关系数据库模式满足第三范式 3NF 。可以认为当前模式满足 3NF，并且能够满足用户的功能需求，不需要进行模式修正。

## 核心代码解析

### 仓库地址

[Ltryxcy/DataBase_Lab (github.com)](https://github.com/Ltryxcy/DataBase_Lab)

### 目录

```latex
├─BankSys
│  ├─BankSys  ------系统的配置文件
│  │  └─__pycache__
│  ├─frontend  -------首页的前端文件
│  │  ├─migrations
│  │  ├─templates
│  │  │  └─frontend
│  │  └─__pycache__
│  ├─media  ------数据库存储员工照片
│  │  └─photos
│  │      ├─20240603
│  │      ├─20240604
│  │      ├─20240605
│  │      └─20240607
│  └─myBankSystem  ------银行管理系统应用
│      ├─migrations  ------存放迁移文件
│      │  └─__pycache__
│      ├─sql  ------存放触发器的SQL代码
│      ├─static
│      │  └─css
│      ├─templates  ------渲染界面的HTML模板
│      │  ├─frontend
│      │  └─myBankSystem
│      └─__pycache__
└─media
    └─photo  ------存放要上传的图片
```

### 1. 客户

> 首先，定义客户的模型，其中身份证号 `id` 是主码且不能为空还不能重复，其他属性分别是姓名、电话号码、邮箱和名下账户数。特别地，为了在网页中登入登出，每个客户需要和一个 `User` 形成一对一联系，这个 `User` 是 Django 提供的用户类，可以提供网页登录的 username 和 password 等信息。

```python
# myBankSystem/models.py
# 客户（<u>身份证号</u>，姓名，手机号，邮箱，名下账户数）
class Bank_Customer(models.Model):
    id = models.CharField(max_length=18, primary_key=True, null=False, unique=True)
    name = models.CharField(max_length=20, null=False)
    tel = models.CharField(max_length=11, null=False)
    email = models.EmailField(max_length=50, blank=True) # 邮箱可以为空
    accounts_cnt = models.IntegerField(default=0) # 名下账户数默认为0
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='BankCustomer', null=True)
    
    def __str__(self):
        return f"{self.id}-{self.name}"
```

#### 1.1 创建客户

> 接下来，通过几个视图函数来实现客户的注册、登录、修改密码、修改客户信息和删除客户等操作。首先是客户注册，如果是 `‘POST’` 请求，先创建一个客户创建的表单，声明创建客户时需要填写的字段，然后调用 Django 中提供的用户注册表单进行用户创建，填写表单相应的字段并且创建新的用户和客户，同时进行登录。如果是 `‘GET’` 请求，那么通过表单获取要填写的字段并渲染即可。

```python
# myBankSystem/forms.py
#   注册表单,包含身份证号，姓名，电话号码，邮箱，名下账户数       
class BankCustomer_RegisterForm(forms.ModelForm):
    id = forms.CharField(label='身份证号', strip=True, error_messages={'required': '身份证号不能为空。'})
    name = forms.CharField(label='姓名', strip=True, error_messages={'required': '姓名不能为空。'})
    tel = forms.CharField(label='电话号码', strip=True, error_messages={'required': '电话号码不能为空。'})
    # 邮箱可以为空
    email = forms.EmailField(label='邮箱')
    account_cnt = forms.IntegerField(label='名下账户数', initial=0, disabled=True)
    class Meta:
       model = Bank_Customer
# myBankSystem/views.py
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
```

#### 1.2 客户登录和修改密码

> 用户登录和修改用户密码，这两个功能主要都是和 `User` 部分相关，都是先创建一个表单，声明需要传递的信息，然后按照上面类似的思路处理 `POST` 和 `GET` 请求。

```python
# myBankSystem/views.py
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
```

#### 1.3 修改客户信息

> 首先，创建一个用于客户编辑个人信息的表单，然后根据用户的 `user_id` 来找到对应的用户和客户，根据是否是当前客户或者管理员来判断是否有权限修改信息。接下来的步骤和之前类似，判断请求的类型，如果是 `POST` 请求，则根据表单中获取的信息修改客户信息；如果是 `GET` 请求，则展示修改信息界面。

```python
# myBankSystem/forms.py
#   编辑表单,包含身份证号，姓名，电话号码，邮箱      
class BankCustomer_EditForm(forms.ModelForm):
    # 不能修改身份证号
    id = forms.CharField(label='身份证号', strip=True, disabled=True)
    # 姓名不能为空
    name = forms.CharField(label='姓名', strip=True, error_messages={'required': '姓名不能为空。'})
    # 电话号码不能为空
    tel = forms.CharField(label='电话号码', strip=True, error_messages={'required': '电话号码不能为空。'})
    # 邮箱可以为空
    email = forms.EmailField(label='邮箱', required=False)
    class Meta:
        model = Bank_Customer
        fields = ('id', 'name', 'tel', 'email')
        
# myBankSystem/views.py
@login_required
def edit_customer(request, user_id):
    # 获取用户
    customer = get_object_or_404(User, id=user_id)
    information = get_object_or_404(Bank_Customer, user_id=user_id)
    # 如果用户不是当前用户，且不是管理员，没有权限修改信息
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
```

#### 1.4 查看客户信息

> 客户可以查看自己的个人信息，通过 `user_id` 得到客户对应的用户，然后根据用户找到客户信息并展示出来。

```python
# myBankSystem/views.py
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
```

#### 1.5 管理员部分

> 在我们实现的系统中，存在管理员和客户两种用户。客户只能查看和修改自己的信息和一些公共的信息，比如支行信息和部门信息。而管理员拥有最高权限，可以查看并修改所有的客户信息，可以删除客户、创建删除支行和部门以及员工等等。本实验中，采用了 Django 自带的 `superuser` 作为管理员。创建管理员步骤如下：
>
> 1. 在终端（BankSys目录下）中输入命令 `py ./manage createsuperuser`
> 2. 根据提示设置管理员账户名和密码，本实验中分别设置为 `username: admin` 和 `password: 12345678`
>
> 下面，是需要管理员权限的两个操作，查看所有客户信息和删除客户。
>
> 通过 `Bank_Customer.objects.all()` 得到所有的客户，然后调用 `Paginator` 进行分页，将分页后的信息作为 context 传入模板中渲染显示。

```py
# myBankSystem/views.py
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
```

> 先通过参数中的 `user_id` 来得到用户和客户。删除客户前需要进行一些判断，如果客户名下还有账户或者未还清的贷款，则不能删除客户。

```python
# myBankSystem/views.py
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
```

### 2. 银行支行

> 首先，定义支行的模型，设置支行的属性，支行名称是主码且非空，另外两个属性是支行所在城市和支行电话。

```python
# myBankSystem/models.py  支行信息表
class Bank_Branch(models.Model):
    # 支行名称是主码且不能为空
    branch_name = models.CharField(max_length=30, primary_key=True, null=False)
    # 支行所在城市
    branch_city = models.CharField(max_length=30)
    # 支行电话
    branch_tel = models.CharField(max_length=11)
    
    def __str__(self):
        return f"{self.branch_name}" # 返回支行名称
```

#### 2.1 显示支行信息

> 添加视图函数来实现增删改查的功能，先定义 `branches` 函数来显示已有支行的信息，按照 6 个支行一页进行分页处理并在网页端显示。

```python
# myBankSystem/views.py
def branches(request):
    # 获取所有支行信息并按支行名称排序
    branches_lists = Bank_Branch.objects.all().order_by('branch_name') 
    paged = Paginator(branches_lists, 6) # 分页，每页显示6条数据
    branches_page = paged.get_page(request.GET.get('page')) # 获取当前页码
    context = {'branches': branches_page}
    # 返回支行管理界面
    template = loader.get_template('myBankSystem/branches.html')
    return HttpResponse(template.render(context, request))
```

#### 2.2 创建支行

> 需要管理员权限，如果是 `‘POST’` 方法，那么需要读取请求中的数据，根据这些数据填写表单，验证表单是否合法，然后保存并提交表单；如果是 `‘GET’` 方法，说明是访问创建支行的界面，获取一个字段未填充的表单。最后，将表单由模板进行渲染显示。

```python
# myBankSystem/forms.py
#  创建支行表单，包含支行名称，支行地址，负责人，联系电话
class Branch_Creation_Form(forms.ModelForm):
    class Meta:
        model = Bank_Branch
        fields = ['branch_name', 'branch_city', 'branch_tel']    
# myBankSystem/views.py
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
```

#### 2.3 删除支行

> 同样需要登录状态和管理员权限。删除支行前需要检查支行下是否存在部门和未还完的贷款，只有当二者都不存在时才能删除支行。

```python
# myBankSystem/forms.py
# 删除支行，需要登录状态，管理员权限
@login_required
def delete_branch(request, branch_name):
    if not request.user.is_superuser:
        return render(request, 'myBankSystem/error.html', {'error': '没有权限删除支行'})
    branch = Bank_Branch.objects.get(branch_name=branch_name)
    if Bank_Department.objects.filter(branch=branch_name).exists():
        return render(request, 'myBankSystem/error.html', {'error': '支行下有部门，无法删除'})
    # 有未还完的贷款
    if Loan.objects.filter(branch=branch_name).exists():
        return render(request, 'myBankSystem/error.html', {'error': '支行下有未还完的贷款，无法删除'})
    branch.delete()
    return redirect('myBankSystem:branches')
```

#### 2.4 修改支行信息

> 需要登录状态和管理员权限，先创建一个修改支行信息的表单，然后通过参数中的支行名称找到对应支行的实体，如果是 `‘POST’` 请求，就填写表单，判断表单是否合法，合法就保存并提交表单；如果是 `‘GET’` 请求，就获取一个未填写字段的表单，处理和前面创建支行类似，要注意的是，作为主码的支行名称是不能修改的，在代码中要有对应的设置。

```python
# myBankSystem/forms.py
class Branch_Edit_Form(forms.ModelForm):
    class Meta:
        model = Bank_Branch
        fields = ['branch_name', 'branch_city', 'branch_tel']
        widgets = {
            'branch_name': forms.TextInput(attrs={'disabled': True}), # 不能修改支行名称
        }
# myBankSystem/views.py
# 修改支行信息，需要登录状态，管理员权限
@login_required
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
```

###  3. 账户

> 根据ER图，有了支行和客户之后，客户就可以在支行下创建账户。首先，定义账户的模型，其中 `account_id` 是主码，并且在创建账户时自动生成，账户的属性包含账户余额、开户时间、所属支行和用户。其中，账户余额不能小于0，开户时间会自动设置为创建账户的时间，所属支行和用户是从支行和客户得到的外键约束。

```python
# myBankSystem/models.py
# 账户（<u>账户号</u>，账户余额，开户时间，身份证号，支行名称）
class Customer_Account(models.Model):
    account_id = models.AutoField(primary_key=True, null=False)
    # 账户余额不能为负数
    money = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    # 开户时间
    create_date = models.DateTimeField(auto_now_add=True)
    # 支行名称，存在外键关联，设置为级联删除
    branch = models.ForeignKey(Bank_Branch, on_delete=models.CASCADE, related_name='BranchAccount')
    user = models.ForeignKey(Bank_Customer, on_delete=models.CASCADE, related_name='CustomerAccount',default='0')
    
    def __str__(self):
        return f"{self.account_id}-{self.user.name}"
```

#### 3.1 创建账户

> 要求处于登录状态，首先通过 `user_id` 找到对应的客户，判断是否是本人创建账户。先创建一个 `Customer_Accounts_Form` 表单，如果是访问创建界面，那么通过模板渲染一个创建账户的界面；如果是 `‘POST’` 请求，那么将请求中的数据填入表单中，如果表单合法，从表单中获取账户余额、所属支行的信息，通过 `Customer_Account.objects.create(user=user, branch=branch, money=account_money)` 创建一个具有指定值的账户。同时，自动增加客户名下的账户数和自动为账户创建一条交易记录，记录账户创建的初始金额等。

```python
# myBankSystem/forms.py
#  账户表单，包含账户号，账户类型，开户时间，余额，所属支行，所属客户
class Customer_Accounts_Form(forms.ModelForm):
    # customer = forms.ModelChoiceField(label='所属客户', queryset=Bank_Customer.objects.all(), disabled=True)
    customer = forms.ModelChoiceField(
        label='所属客户', 
        queryset=Bank_Customer.objects.none(),
        disabled=True)
    branches = forms.ModelChoiceField(label='所属支行', queryset=Bank_Branch.objects.all())
    account_money = forms.FloatField(label='余额', min_value=0.0)
    
    class Meta:
        model = Customer_Account
        fields = ('customer', 'branches', 'account_money')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set the customer field to disabled and add the required attribute
        self.fields['customer'].disabled = False
        self.fields['customer'].required = True
        self.fields['branches'].required = True
        self.fields['account_money'].required = True

# myBankSystem/views.py
# 创建账户，要求处于登录状态
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
```

#### 3.2 查询账户信息

> 客户可以查询自己名下的账户信息，首先通过 `user_id` 得到拥有账户的客户，然后通过 `Customer_Account.objects.filter(user_id=account_user.id)` 过滤出当前客户名下的所有账户，并分页显示账户信息。

```py
# myBankSystem/views.py
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
```

#### 3.3 删除账户（触发器）

> 需要处于登录状态，并且客户只能删除自己名下的账户。如果账户中余额大于0，那么无法删除，同时设计触发器，当账户表增加行时，会自动更新对应客户名下的账户数量。

```python
# myBankSystem/views.py
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
        return render(request, 'myBankSystem/error.html', {'error': '无法删除账户，账户中还有余额'})
    # 触发器，自动更新用户的账户数
    user.save()
    account.delete()
    
    return redirect('myBankSystem:accounts_info', user_id=user.user_id)
```

```sql
# myBankSystem/sql/triggers.sql
DROP TRIGGER IF EXISTS auto_delete;
# 创建触发器，删除账户时自动减少用户的账户数
CREATE Trigger auto_delete
AFTER DELETE ON mybanksystem_customer_account FOR EACH ROW
BEGIN
    UPDATE mybanksystem_bank_customer SET accounts_cnt = accounts_cnt - 1 WHERE id = OLD.user_id;
END;
```

#### 3.4 账户间转账

> 本系统实现了两个账户间的转账操作，这里采用了事务编程，将转账操作写成一个事务。首先，根据账户号得到源账户和拥有账户的客户，创建一个账户交易表单，包含了源账户和目标账户以及转账金额，转账金额不能小于0。如果是 `‘POST'` 请求，那么从表单中获取转账金额和目标账户，判断账户余额是否足够，并且目标账户不能是自己。开启事务块，从源账户扣款，给目标账户增加金额，保存源账户和目标账户信息，最后自动生成两个账户的交易记录，结束事务块。如果事务块中发生错误，Django 会自动回滚到事务块开始前的状态。如果是 `‘GET’` 请求，那么通过表单渲染一个转账界面。

```py
# myBankSystem/forms.py
#  账户转账表单，包含转出账户，转入账户，转账金额
class Accounts_Trade_Form(forms.ModelForm):
    src_account = forms.ModelChoiceField(label='转出账户', queryset=Customer_Account.objects.all(), disabled=True)
    target_account = forms.ModelChoiceField(label='转入账户', queryset=Customer_Account.objects.all())
    trade_money = forms.FloatField(label='转账数额', min_value=0.0)
    class Meta:
        model = Customer_Account
        fields = ('src_account', 'target_account', 'trade_money')
       
# myBankSystem/views.py
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
```

#### 3.5 账户交易

> 这部分实现了客户从账户中存取款的功能。先获取账户和对应的客户，然后创建一个 `Create_Trade_Form` 表单。按照前面的思路分别处理 `POST` 和 `GET` 请求，交易金额可以为正数或负数，正数代表存款，负数代表从账户中取款。同时自动生成对应的交易记录。

```python
# myBankSystem/forms.py
# 创建交易的表单
class Create_Trade_Form(forms.ModelForm):
    trade_type = [('收入', '收入'), ('支出', '支出')]
    account = forms.ModelChoiceField(label='账户信息', queryset=Customer_Account.objects.all(), disabled=True)
    money = forms.FloatField(label='金额')
    type = forms.ChoiceField(label='类型', choices=trade_type)
    detail = forms.CharField(label='详情', required=False)
    class Meta:
        model = Transactions
        fields = ('account', 'money', 'type', 'detail')

# myBankSystem/views.py
# 转入/取出金额，需要登录状态
@login_required
def create_trade(request, account_id):
    # 获取账户
    account = get_object_or_404(Customer_Account, account_id=account_id)
    # 获取账户的拥有者
    user = get_object_or_404(Bank_Customer, id=account.user.id)
    user_id = user.user_id
    # 判断是否是账户的拥有者
    if request.user.id != user_id:
        return render(request, 'myBankSystem/error.html', {'error': '您没有此账户权限！'})
    if request.method != 'POST':
        form = Create_Trade_Form(initial={'account': account})
    else:
        form = Create_Trade_Form(data=request.POST, initial={'account': account})
        if form.is_valid():
            # 获取交易前的账户余额
            pre_money = account.money
            trade_money = form.cleaned_data['money']
            trade_type = form.cleaned_data['type']
            trade_detail = form.cleaned_data['detail']
            money = pre_money + trade_money
            if money < 0:
                return render(request, 'myBankSystem/error.html', {'error': '余额不足'})
            transaction = Transactions.objects.create(account=account, money=trade_money, transaction_type=trade_type, transaction_detail=trade_detail)
            # 保存交易记录
            transaction.save()
            # 更新账户余额
            account.money = money
            account.save()
            return redirect('myBankSystem:transactions_info', account_id=account_id)
        else:
            logger.error(f"Form is not valid: {form.errors}")
            return render(request, 'myBankSystem/error.html', {'error': '输入不合法'})
    context = {'form': form, 'account': account}
    return render(request, 'myBankSystem/create_trade.html', context)
```

### 4. 交易记录

> 每当交易完成时自动生成对应的交易记录，即在交易的存储过程中创建交易记录，不支持交易记录的删除，只有当删除账户时才会级联删除账户对应的交易记录。所以只用实现客户查看账户下的交易记录和管理员查看全部交易记录的视图函数。首先，定义交易记录的模型，主码为交易记录号，其他属性有默认为支出的交易类型、交易详情和交易时间，以及存在外键关联的账户。

```python
# myBankSystem/models.py
# 交易记录（<u>交易记录号</u>，修改净值，交易类型，交易详情，账户号，交易时间）
class Transactions(models.Model):
    # 交易记录号为主码且不能为空
    transaction_id = models.AutoField(primary_key=True, null=False)
    # 修改净值
    money = models.FloatField(default=0.0)
    # 交易类型
    types = [
        ('收入', '收入'),
        ('支出', '支出'),
    ]
    # 默认为支出
    transaction_type = models.CharField(max_length=100, choices=types, default='支出')
    # 交易详情
    transaction_detail = models.CharField(max_length=100, blank=True)
    # 账户号，存在外键关联，设置为级联删除
    account = models.ForeignKey(Customer_Account, on_delete=models.CASCADE, related_name='Transactions')
    # 交易时间
    transaction_date = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return f"交易记录号{self.transaction_id}-交易详情{self.transaction_detail}"
```

#### 4.1 客户查询交易记录

> 这里的实现非常简单，只要从 `account_id` 得到账户和对应的客户，然后从交易记录中筛选出属于该账户的记录并分页显示。

```py
# myBankSystem/views.py
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
```

#### 4.2 管理员查看交易记录

> 先判断是否是管理员，然后按照交易记录号的顺序获取所有的交易记录，并按照每页 6 条记录进行分页显示。

```py
# myBankSystem/views.py
# 显示所有的交易记录，需要登录状态，管理员权限
@login_required
def transactions_list(request):
    if not request.user.is_superuser:
        return render(request, 'myBankSystem/error.html', {'error': '没有权限查看交易记录'})
    # 获取所有的交易记录
    transactions_list = Transactions.objects.all().order_by('transaction_id')
    # 分页，每页显示6条数据
    paged = Paginator(transactions_list, 6)
    transactions_page = paged.get_page(request.GET.get('page'))
    context = {'transactions': transactions_page}
    return render(request, 'myBankSystem/transactions_list.html', context)
```

### 5. 贷款信息

> 除了通过账户交易，客户还可以直接从银行支行申请贷款和偿还贷款。首先，定义贷款的模型，主码为贷款号，其他属性包括贷款总额、贷款日期、还款期限、未还清余额，以及存在外键关联的贷款客户和放贷支行。

```py
# myBankSystem/models.py
#  贷款（<u>贷款号</u>，贷款总额，还款期限，未还清余额，身份证号，支行名称，贷款日期）
class Loan(models.Model):
    # 贷款号为主码且不能为空
    loan_id = models.AutoField(primary_key=True, null=False)
    # 贷款总额
    loan_total = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    # 还款期限
    loan_deadline = models.DateTimeField(default=datetime.now() + timedelta(days=1095))
    # 未还清余额
    loan_balance = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    # 身份证号，存在外键关联，设置为级联删除
    customer = models.ForeignKey(Bank_Customer, on_delete=models.CASCADE, related_name='Loan')
    # 支行名称，存在外键关联，设置为级联删除
    branch = models.ForeignKey(Bank_Branch, on_delete=models.CASCADE, related_name='BranchLoan')
    # 贷款日期
    loan_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"贷款号{self.loan_id}-贷款总额{self.loan_total}"
```

#### 5.1 申请贷款

> 客户可以向支行申请贷款，也是采用提交表单的方式进行数据传递，整体思路和之前创建账户类似，需要注意的是，管理员不具备申请贷款的资格，同时不能为他人申请贷款。

```py
# myBankSystem/forms.py
# 贷款申请表单
class Apply_Loan_Form(forms.ModelForm):
    user = forms.ModelChoiceField(label='客户信息', queryset=Bank_Customer.objects.all(), disabled=True)
    branch = forms.ModelChoiceField(label='所属支行', queryset=Bank_Branch.objects.all(), disabled=True)
    money = forms.FloatField(label='贷款金额', min_value=0.0)
    class Meta:
        model = Loan
        fields = ('user', 'branch', 'money')
# myBankSystem/views.py
# 申请贷款，需要登录状态
@login_required
def apply_loan(request, user_id, branch_name):
    if request.user.is_superuser:
        return render(request, 'myBankSystem/error.html', {'error': '管理员无法申请贷款'})
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
```

#### 5.2 查询贷款信息

> 这一部分实现了两种功能，管理员查看所有贷款信息以及客户查看自己的贷款信息。实现思路和前面查看交易记录非常类似，所以在此不再赘述和展示代码。

#### 5.3 偿还贷款

> 实现了用户还款的功能，也是创建了一个还款表单来传递数据。按照 `POST` 和 `GET`  两种方法处理请求。需要注意的是，在还款的时候，要判断还款金额是否超过未还清金额，如果超过了则需要报错。还款后报错贷款信息，并且检查未还清金额是否为0，如果金额为0，自动删除该条贷款的信息。

```py
# myBankSystem/forms.py
# 还款表单
class Repay_Loan_Form(forms.ModelForm):
    loan = forms.ModelChoiceField(label='贷款信息', queryset=Loan.objects.all(), disabled=True)
    user = forms.ModelChoiceField(label='客户信息', queryset=Bank_Customer.objects.all(), disabled=True)
    branch = forms.ModelChoiceField(label='所属支行', queryset=Bank_Branch.objects.all(), disabled=True)
    repay_money = forms.FloatField(label='还款金额', min_value=0.0)
    class Meta:
        model = Loan
        fields = ('loan', 'user', 'branch', 'repay_money')

# myBankSystem/views.py
# 只展示还款的核心部分
if request.method != 'POST':
        form = Repay_Loan_Form(initial={'loan': loan,'user': user, 'branch': branch})
    else:
        form = Repay_Loan_Form(initial={'loan': loan, 'user': user, 'branch': branch}, data=request.POST)
        if form.is_valid():
            repay_money = form.cleaned_data['repay_money']
            if repay_money > loan.loan_balance:
                return render(request, 'myBankSystem/error.html', {'error': '还款金额大于贷款余额'})
            loan.loan_balance = loan.loan_balance - repay_money
            loan.save()
            # 如果已经还清贷款，自动删除贷款记录
            if loan.loan_balance == 0:
                loan.delete()
            return redirect('myBankSystem:loans_info', user_id=user.user_id)
        else:
            logger.error(f"Form is not valid: {form.errors}")
            return render(request, 'myBankSystem/error.html', {'error': '输入不合法'})
```

### 6. 银行部门

> 每个支行下辖多个部门，先定义部门的模型，其中主码为部门号，其他属性有部门名称和部门经理，以及存在外键约束的所属支行。

```py
# myBankSystem/models.py
# 银行部门（部门号，支行名称，部门名称，部门经理）
class Bank_Department(models.Model):
    # 部门号是主码且不能为空
    department_id = models.AutoField(primary_key=True, null=False)
    # 部门所属支行，存在外键关联，设置为级联删除
    branch = models.ForeignKey(Bank_Branch, on_delete=models.CASCADE, related_name='Bank_department')
    # 部门名称
    department_name = models.CharField(max_length=30, null=False)
    # 部门经理
    department_manager = models.CharField(max_length=20, null=True,blank=True)
    
    def __str__(self):
        return f"{self.branch.branch_name}-{self.department_name}"
```

#### 6.1 创建部门

> 只有管理员才能创建部门，部门创建的信息通过表单进行传递。部门创建的表单中提供了可选的支行字段，部门经理可以设为 `None`。部门创建的实现和之前创建支行比较类似，这里不再赘述。

```py
# myBankSystem/forms.py
# 部门创建表单
class Department_Creation_Form(forms.ModelForm):
    branch = forms.ModelChoiceField(label='所属支行', queryset=Bank_Branch.objects.all())
    department_name = forms.CharField(label='部门名称', max_length=20)
    class Meta:
        model = Bank_Department
        fields = ['department_name', 'department_manager', 'branch']
        widgets = {
            'department_name': forms.TextInput(attrs={'class': 'input'}),
            'department_manager': forms.TextInput(attrs={'class': 'input'}),
            'branch': forms.HiddenInput(),
        }
```

#### 6.2 查询部门信息

> 所有人都能查询部门信息，但是会有一些属性只有管理员才能看到，比如部门号。部门信息的查询和支行信息查询非常相似，区别在于需要添加部门经理这个属性，要遍历部门和部门经理，把部门经理填入对应的部门中。

```py
# myBankSystem/views.py departments函数，这里只展示比较不同的部分
	departments_page = paged.get_page(request.GET.get('page'))
    managers = Department_Manager.objects.all() # 获取所有部门经理
    # 遍历部门信息，将部门经理添加到部门信息中
    for department in departments_page:
        for manager in managers:
            if department.department_id == manager.departments.department_id:
                department.department_manager = manager.staffs.staff_name
    context = {'departments': departments_page}
```

#### 6.3 修改部门信息

> 需要管理员权限，通过一个表单实现数据传递。其中部门号不能修改，部门经理的设置在后面部分实现，所以这里只能修改所属支行和部门名称。因为视图函数的实现和前面的修改信息非常类似，这里只展示表单。

```py
# myBankSystem/forms.py
# 部门编辑表单
class Department_Edit_Form(forms.ModelForm):
    department_id = forms.IntegerField(label='部门号', disabled=True)
    branch = forms.ModelChoiceField(label='所属支行', queryset=Bank_Branch.objects.all())
    department_name = forms.CharField(label='部门名称', max_length=20)
    class Meta:
        model = Bank_Department
        fields = ['department_id', 'department_name', 'branch']
        widgets = {
            'department_id': forms.TextInput(attrs={'class': 'input'}),
            'department_name': forms.TextInput(attrs={'class': 'input'}),
            'branch': forms.HiddenInput(),
        }
```

#### 6.4 删除部门

> 需要管理员权限，同时满足部门内没有员工的条件。

```py
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
```

### 7. 员工

> 在本系统中，员工必须要归属于一个部门，并且员工有一个子类为部门经理。首先，定义员工和部门经理的模型，员工的主码为工号，其他属性有姓名、性别、电话和照片，这里通过照片体现系统对图片的管理，还有一个外键关联，即员工所属部门。子类部门经理和员工之间存在一个一对一关系，因为部门经理本身也是员工，所以部门经理一定会和一个员工存在一对一关系。同时，部门经理还和部门存在外键约束。

```py
# myBankSystem/models.py
# 员工（<u>工号</u>，员工照片，姓名，性别，手机号，部门号）
class Bank_Staff(models.Model):
    # 工号为主码且不能为空
    staff_id = models.AutoField(primary_key=True, null=False)
    # 员工照片
    staff_photo = models.ImageField(upload_to='photos/%Y%m%d/', default='photos/default.jpg')
    # 姓名
    staff_name = models.CharField(max_length=20, null=False)
    # 性别
    staff_sex = models.CharField(max_length=10, null=False)
    # 手机号
    staff_tel = models.CharField(max_length=11, null=False)
    # 部门号，存在外键关联，设置为级联删除
    department = models.ForeignKey(Bank_Department, on_delete=models.CASCADE, related_name='DepartmentStaff')
    def __str__(self):
        return f"{self.staff_id}-{self.staff_name}"
    
# 部门经理（<u>工号</u>，部门号）
class Department_Manager(models.Model):
    departments = models.ForeignKey(Bank_Department, on_delete=models.CASCADE, related_name='departments_manager')
    staffs = models.OneToOneField(Bank_Staff, on_delete=models.CASCADE, related_name='staffs_manager')
    def __str__(self):
        return f"{self.staffs.staff_id}-{self.staffs.staff_name}"
```

#### 7.1 创建员工

> 通过一个表单来传递创建员工的信息。创建员工时，从表单中获取各字段的信息并填入数据库中，先根据所属部门、姓名、电话和性别创建一个员工，然后再从请求的文件部分获取照片，如果没有找到照片，那么会采用默认照片。这里只展示与前面创建功能不同的部分。管理媒体文件需要在`BankSys/settings.py`中增加没积文件的URL路径和存储媒体文件的根目录，实现如下：

```py
# BankSys/settings.py
# 媒体文件的URL路径
MEDIA_URL = '/media/'
# 媒体文件存储的根目录
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# myBankSystem/forms.py
# 员工创建表单
class Staff_Creation_Form(forms.ModelForm):
    department = forms.ModelChoiceField(label='所属部门', queryset=Bank_Department.objects.all(),widget=forms.HiddenInput())
    name = forms.CharField(label='姓名', max_length=20)
    tel = forms.CharField(label='电话', max_length=11)
    photo = forms.ImageField(label='照片', required=False)
    sex = forms.ChoiceField(label='性别', choices=[('男', '男'), ('女', '女')])
    class Meta:
        model = Bank_Staff
        fields = ('department', 'name', 'tel', 'photo', 'sex')
# myBankSystem/views.py  create_staff函数
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
```

#### 7.2 查询员工信息

> 需要管理员权限，这部分实现了两种查询方法，一种是在每个部门下查看部门员工，另一种是直接查看所有员工信息。具体实现跟前面展示过的非常类似，不再赘述。

#### 7.3 删除员工

> 需要管理员权限，通过 `staff_id` 找到对应员工，删除前考虑是否是部门经理，如果是部门经理，那么在子类部门经理中也要删除该经理。同时，检查员工照片是否是默认照片，如果不是默认照片，那么在数据库中也删除掉该员工的照片，最后，删除该员工。

```py
# myBankSystem/views.py
@login_required
def delete_staff(request, staff_id):
    # 查看是否有权限
    if not request.user.is_superuser:
        return render(request, 'myBankSystem/error.html', {'error': '没有权限删除员工'})
    # 找到对应员工
    staff = Bank_Staff.objects.get(staff_id=staff_id)
    department = staff.department
    # 删除员工，考虑是否是部门经理
    if Department_Manager.objects.filter(staffs_id=staff_id):
        manager = Department_Manager.objects.get(staffs_id=staff_id)
        manager.delete()
    # 删除员工照片
    if staff.staff_photo.name != '/photos/default.jpg':
        staff.staff_photo.delete()
    staff.delete()
    return redirect('myBankSystem:department_staff', department_id=department.department_id)
```

#### 7.4 修改员工信息

> 这部分实现了修改员工的姓名、性别、电话、所属部门和照片的功能。依然是通过一个表单在网页端和后端传递信息，表单中的字段中所属部门和性别要在已有选项中选择，其他字段均可自由修改。

```py
# myBankSystem/forms.py
class Staff_Edit_Form(forms.ModelForm):
    staff_id = forms.IntegerField(label='工号', disabled=True)
    department = forms.ModelChoiceField(label='所属部门', queryset=Bank_Department.objects.all())
    name = forms.CharField(label='姓名', max_length=20)
    tel = forms.CharField(label='电话', max_length=11)
    photo = forms.ImageField(label='照片', required=False)
    sex = forms.ChoiceField(label='性别', choices=[('男', '男'), ('女', '女')])
```

> 通过工号来查询到对应的员工，这里主要讲`POST`请求。从表单中获取修改的信息，填入对应的字段中。要考虑一种特殊情况，即员工原来是部门经理但是更换了部门，这时要先从部门经理中找到该员工，删除其在原部门的部门经理子类。如果提交了新的照片，需要检查原来照片是否是默认照片，如果不是，则删除原有照片，填入新照片。最后，保存修改。

```py
# myBankSystem/views.py
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
```

#### 7.5 设置部门经理

> 需要管理员权限，先根据传入的参数确定员工和员工所在部门，检查部门是否已经有经理，如果已有经理，则报错；否则，根据得到的员工和部门创建部门经理并保存。

```py
# myBankSystem/views.py
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
    manager = Department_Manager(departments=department, staffs=staff)
    manager.save()
    return redirect('myBankSystem:departments')
```

#### 7.6 删除部门经理

> 需要管理员权限，先根据部门号找到对应部门并获取部门经理，如果没有经理，则输出错误信息；否则，直接删除该部门经理。

```py
# myBankSystem/views.py
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
    else:
        return render(request, 'myBankSystem/error.html', {'error': '部门无经理'})
    return redirect('myBankSystem:departments')
```

## 实验与测试

### 依赖

> - Python 3.12.3
> - Django 5.0.6
> - Bulma 1.0.1

### 部署

> Windows环境下，命令行中先运行 `py manage.py makemigrations` 生成迁移文件，再运行 `py manage.py migrate` 执行迁移。通过 `py manage.py createsuperuser` 来设置自己的管理员账号。命令行中输入 `py manage.py runserver` 启动系统，在浏览器中访问界面即可。

### 实验结果

#### 1.1 首页

![image-20240605210000738](C:\Users\86134\AppData\Roaming\Typora\typora-user-images\image-20240605210000738.png)

#### 1.2 客户注册

![image-20240605211141365](C:\Users\86134\AppData\Roaming\Typora\typora-user-images\image-20240605211141365.png)

> 输入的信息如图所示，其中密码为ustc1958，注册成功后跳转到登录状态下的首页。

![image-20240605211521537](C:\Users\86134\AppData\Roaming\Typora\typora-user-images\image-20240605211521537.png)

#### 1.3 客户登录

> 客户登录界面如下，登录成功后依然回到登录状态下的首页

![image-20240605211648179](C:\Users\86134\AppData\Roaming\Typora\typora-user-images\image-20240605211648179.png)

#### 1.4 客户修改密码

> 修改密码界面如下，将密码修改为1958ustc

![image-20240605211820927](C:\Users\86134\AppData\Roaming\Typora\typora-user-images\image-20240605211820927.png)

> 修改密码后自动退出登录，需要用新密码重新登录

![image-20240605211850732](C:\Users\86134\AppData\Roaming\Typora\typora-user-images\image-20240605211850732.png)

#### 1.5 查询个人信息

> 点击个人信息按钮，可以查询到用户当前的个人信息

![image-20240605211931398](C:\Users\86134\AppData\Roaming\Typora\typora-user-images\image-20240605211931398.png)

#### 1.6  修改个人信息

> 在修改个人信息界面，身份证号是不能修改的，其他信息均可修改，这里把姓名修改为小李，可以看到信息修改成功。

![image-20240605212108804](C:\Users\86134\AppData\Roaming\Typora\typora-user-images\image-20240605212108804.png)

![image-20240605212124170](C:\Users\86134\AppData\Roaming\Typora\typora-user-images\image-20240605212124170.png)

#### 1.7 客户删除

> 登入管理员账号，删除刚刚创建的姓名为小李的客户

![image-20240605212323368](C:\Users\86134\AppData\Roaming\Typora\typora-user-images\image-20240605212323368.png)

> 此时，再尝试用原来的账号登录就会出现错误，因为客户已经被删除

![image-20240605212419796](C:\Users\86134\AppData\Roaming\Typora\typora-user-images\image-20240605212419796.png)

#### 1.8 管理员界面

> 管理员界面如下，可以看到，管理员界面可以查看支行信息、部门信息、客户信息、贷款信息、员工信息和交易记录，其中系统后台是跳转到 Django 自带的管理系统。

![image-20240605213332891](C:\Users\86134\AppData\Roaming\Typora\typora-user-images\image-20240605213332891.png)

#### 2.1 创建支行

> 创建支行界面如下：

![image-20240605213436709](C:\Users\86134\AppData\Roaming\Typora\typora-user-images\image-20240605213436709.png)

> 可以看到，新增了刚刚创建的越秀支行，这里是支行信息显示界面

![image-20240605213500956](C:\Users\86134\AppData\Roaming\Typora\typora-user-images\image-20240605213500956.png)

#### 2.2 修改支行信息

> 进入编辑支行信息界面，可以看到支行名称不能修改，所在城市和联系电话均可修改，现在修改电话为66666

![image-20240605213640953](C:\Users\86134\AppData\Roaming\Typora\typora-user-images\image-20240605213640953.png)

> 修改后越秀支行的信息如下：

![image-20240605213704902](C:\Users\86134\AppData\Roaming\Typora\typora-user-images\image-20240605213704902.png)

#### 2.3 删除支行

> 删除刚刚创建的越秀支行

![image-20240605213728488](C:\Users\86134\AppData\Roaming\Typora\typora-user-images\image-20240605213728488.png)

> 同时尝试删除名下有未还清贷款或账户的支行城南支行，会出现错误提示界面

![image-20240605213846755](C:\Users\86134\AppData\Roaming\Typora\typora-user-images\image-20240605213846755.png)

#### 3.1 创建账户

> 在客户科比名下创建一个开户银行为政务城支行，余额为20000的账户

![image-20240605214054730](C:\Users\86134\AppData\Roaming\Typora\typora-user-images\image-20240605214054730.png)

#### 3.2 账户信息显示

> 在账户信息界面可以看到新创建的账户

![image-20240605214125010](C:\Users\86134\AppData\Roaming\Typora\typora-user-images\image-20240605214125010.png)

#### 3.3 删除账户和账户交易转账

> 直接尝试删除账户号为6的账户，会出现错误

![image-20240605214259204](C:\Users\86134\AppData\Roaming\Typora\typora-user-images\image-20240605214259204.png)

> 先从账户号为6的账户中向账户号为3的账户转账10000元，可以看到两个账户余额都发生变化

![image-20240605214433518](C:\Users\86134\AppData\Roaming\Typora\typora-user-images\image-20240605214433518.png)

![image-20240605214448785](C:\Users\86134\AppData\Roaming\Typora\typora-user-images\image-20240605214448785.png)

> 再从账户号为6的账户中取出10000元

![image-20240605214533584](C:\Users\86134\AppData\Roaming\Typora\typora-user-images\image-20240605214533584.png)

> 此时账户6中余额为0

![image-20240605214626029](C:\Users\86134\AppData\Roaming\Typora\typora-user-images\image-20240605214626029.png)

> 查看账户6的交易记录，符合我们的操作

![image-20240605214700930](C:\Users\86134\AppData\Roaming\Typora\typora-user-images\image-20240605214700930.png)

> 此时再尝试删除账户号为6的账户，删除成功，此时kobe名下只有一个账户

![image-20240605214735187](C:\Users\86134\AppData\Roaming\Typora\typora-user-images\image-20240605214735187.png)

#### 4. 交易记录

> 刚刚已经展示了客户端查看交易记录，这里仅展示管理员端的交易记录查看，管理员能看到所有账户的交易记录。

![image-20240605215204833](C:\Users\86134\AppData\Roaming\Typora\typora-user-images\image-20240605215204833.png)

#### 5.1 申请贷款

> 向政务城支行申请贷款，贷款金额为100元

![image-20240605215341241](C:\Users\86134\AppData\Roaming\Typora\typora-user-images\image-20240605215341241.png)

#### 5.2 查看贷款信息

> 可以在贷款信息界面查看到刚刚申请的100元贷款和之前申请的未还清的贷款

![image-20240605215437042](C:\Users\86134\AppData\Roaming\Typora\typora-user-images\image-20240605215437042.png)

#### 5.3 偿还贷款

> 还清刚刚申请的100元贷款，还清后自动删除了贷款信息

![image-20240605215550485](C:\Users\86134\AppData\Roaming\Typora\typora-user-images\image-20240605215550485.png)

![image-20240605215615261](C:\Users\86134\AppData\Roaming\Typora\typora-user-images\image-20240605215615261.png)

#### 6.1 创建部门

> 为天河支行创建财务部，部门经理暂时为空

![image-20240605215757490](C:\Users\86134\AppData\Roaming\Typora\typora-user-images\image-20240605215757490.png)

#### 6.2 查看部门信息

> 在部门信息界面可以看到刚刚创建的财务部，部门ID为4，部门经理暂缺

![image-20240605215854764](C:\Users\86134\AppData\Roaming\Typora\typora-user-images\image-20240605215854764.png)

#### 6.3 修改部门信息

> 将部门名修改为法务部，

![image-20240605215946259](C:\Users\86134\AppData\Roaming\Typora\typora-user-images\image-20240605215946259.png)

> 可以看到部门名已经修改，信息修改成功

![image-20240605215955761](C:\Users\86134\AppData\Roaming\Typora\typora-user-images\image-20240605215955761.png)

#### 6.4 删除部门

> 删除刚刚创建的法务部，并且尝试删除有员工的安保部门

![image-20240605220128111](C:\Users\86134\AppData\Roaming\Typora\typora-user-images\image-20240605220128111.png)

> 可以看到，没有部门员工的法务部顺利删除，而安保部门由于有员工所以无法删除

![image-20240605220205654](C:\Users\86134\AppData\Roaming\Typora\typora-user-images\image-20240605220205654.png)

#### 7.1 创建员工

> 创建一个名为柯南的员工并暂时不传照片

![image-20240605220507853](C:\Users\86134\AppData\Roaming\Typora\typora-user-images\image-20240605220507853.png)

#### 7.2 显示员工信息

> 在该部门员工中可以看到使用了默认照片的员工柯南

![image-20240605220545101](C:\Users\86134\AppData\Roaming\Typora\typora-user-images\image-20240605220545101.png)

#### 7.3 编辑员工信息

> 这里体现了对员工照片文件的管理，修改员工照片，其他信息不做修改。

![image-20240605220652492](C:\Users\86134\AppData\Roaming\Typora\typora-user-images\image-20240605220652492.png)

> 可以看到员工照片变为了我们上传的照片，并且在指定的存放媒体文件的文件夹中出现了该照片

![image-20240605220728427](C:\Users\86134\AppData\Roaming\Typora\typora-user-images\image-20240605220728427.png)

![image-20240605220810555](C:\Users\86134\AppData\Roaming\Typora\typora-user-images\image-20240605220810555.png)

#### 7.4 设置经理

> 将柯南设为技术部门的经理

![image-20240605220858826](C:\Users\86134\AppData\Roaming\Typora\typora-user-images\image-20240605220858826.png)

#### 7.5 取消经理

> 取消业务办理部小美的经理职务

![image-20240605220940382](C:\Users\86134\AppData\Roaming\Typora\typora-user-images\image-20240605220940382.png)

### 关于存储过程、函数、触发器和事务的说明

在本次实验中，由于 Django 强大的功能，并没有显式地通过 SQL 语言来编写存储过程和函数。在转账中，我将两方账户的余额改变和账单创建都放入一个事务块中，一旦失败 Django 提供的自动回滚功能可以回滚到事务块开始前，这里实现了事务。存储过程和函数主要通过视图函数实现。触发器部分是在删除账户部分实现的，通过一个用 `SQL` 语言编写的触发器来实现删除账户时对应客户名下的账户数的自动修改。

## 参考

- Django 官方文档[Getting started with Django | Django (djangoproject.com)](https://www.djangoproject.com/start/)
- 前端模板采用的是 Bulma 框架 https://bulma.io/documentation/start

- Django 提供的示例指引也非常有帮助 [编写你的第一个 Django 应用，第 1 部分 | Django 文档 | Django (djangoproject.com)](https://docs.djangoproject.com/zh-hans/5.0/intro/tutorial01/)