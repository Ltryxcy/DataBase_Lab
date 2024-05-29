from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from datetime import datetime, timedelta
# Create your models here.

# 支行信息表
class Bank_Branch(models.Model):
    # 支行名称是主码且不能为空
    branch_name = models.CharField(max_length=30, primary_key=True, null=False)
    # 支行所在城市
    branch_city = models.CharField(max_length=30)
    # 支行电话
    branch_tel = models.CharField(max_length=11)
    # 支行负责人
    branch_manager = models.CharField(max_length=20)
    
    def __str__(self):
        return f"{self.branch_name}" # 返回支行名称
    
# 银行部门（部门号，支行名称，部门名称，部门经理）
class Bank_Department(models.Model):
    # 部门号是主码且不能为空
    department_id = models.AutoField(primary_key=True, null=False)
    # 部门所属支行，存在外键关联，设置为级联删除
    branch = models.ForeignKey(Bank_Branch, on_delete=models.CASCADE, related_name='Bank_department')
    # 部门名称
    department_name = models.CharField(max_length=30, null=False)
    # 部门经理
    department_manager = models.CharField(max_length=20)
    
    def __str__(self):
        return f"{self.branch.branch_name}-{self.department_name}"
    
# 员工（<u>工号</u>，员工照片，姓名，性别，手机号，部门号）
class Bank_Staff(models.Model):
    # 工号为主码且不能为空
    staff_id = models.AutoField(primary_key=True, null=False)
    # 员工照片
    staff_photo = models.ImageField(upload_to='photos/%Y%m%d/', default='photos/GGbond.jpg')
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

# 支行负责人（<u>工号</u>，支行名称）
class Branch_Manager(Bank_Staff):
    # 支行负责人是员工的子类
    branch_name = models.ForeignKey(Bank_Branch, on_delete=models.CASCADE, related_name='BranchManager')
    
    def __str__(self):
        return f"{self.staff_id}-{self.staff_name}"
    
# 部门经理（<u>工号</u>，部门号）
class  Department_Manager(Bank_Staff):
    # 部门经理是员工的子类
    dept_id = models.ForeignKey(Bank_Department, on_delete=models.CASCADE, related_name='DepartmentManager')
    
    def __str__(self):
        return f"{self.staff_id}-{self.staff_name}"
    
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

# 账户（<u>账户号</u>，账户余额，开户时间，身份证号，支行名称）
class Customer_Account(models.Model):
    account_id = models.AutoField(primary_key=True, null=False)
    # 账户余额不能为负数
    money = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])
    # 开户时间
    create_date = models.DateTimeField(auto_now_add=True)
    # 身份证号，存在外键关联，设置为级联删除
    customer = models.ForeignKey(Bank_Customer, on_delete=models.CASCADE, related_name='CustomerAccount')
    # 支行名称，存在外键关联，设置为级联删除
    branch = models.ForeignKey(Bank_Branch, on_delete=models.CASCADE, related_name='BranchAccount')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='CustomerAccount', null=True)
    
    def __str__(self):
        return f"{self.account_id}-{self.customer.name}"

# 交易记录（<u>交易记录号</u>，修改净值，交易类型，交易详情，账户号，交易时间）
class Transaction(models.Model):
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
    account = models.ForeignKey(Customer_Account, on_delete=models.CASCADE, related_name='Transaction')
    # 交易时间
    transaction_date = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return f"交易记录号{self.transaction_id}-交易详情{self.transaction_detail}"

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