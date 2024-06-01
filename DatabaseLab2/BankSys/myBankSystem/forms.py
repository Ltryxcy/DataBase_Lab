from django import forms
from django.contrib.auth.models import User
from .models import Bank_Customer, Customer_Account, Bank_Staff, Bank_Branch, Transactions

# 登录只有用户名和密码两个字段
class BankCustomer_LoginForm(forms.Form):
    username = forms.CharField(label='用户名', strip=True, error_messages={'required': '用户名不能为空。'})
    # 密码字段，允许空格，输入时隐藏密码
    password = forms.CharField(label='密码', strip=False, error_messages={'required': '密码不能为空。'}, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password')
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
       fields = ('id', 'name', 'tel', 'email', 'account_cnt') 
       
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

#  账户转账表单，包含转出账户，转入账户，转账金额
class Accounts_Trade_Form(forms.ModelForm):
    src_account = forms.ModelChoiceField(label='转出账户', queryset=Customer_Account.objects.all(), disabled=True)
    target_account = forms.ModelChoiceField(label='转入账户', queryset=Customer_Account.objects.all())
    trade_money = forms.FloatField(label='转账数额', min_value=0.0)
    class Meta:
        model = Customer_Account
        fields = ('src_account', 'target_account', 'trade_money')
    
##  交易记录表单，包含交易记录号，交易金额，交易类型，交易详情，账户号，交易时间
class Account_Transactions_Form(forms.ModelForm):
    transactions_type = [('收入', '收入'), 
                         ('支出', '支出'),]
    account = forms.ModelChoiceField(label='账户信息', queryset=Customer_Account.objects.all(), disabled=True)
    trade_money = forms.FloatField(label='交易金额', min_value=0.0)
    trade_type = forms.ChoiceField(label='交易类型', choices=transactions_type)
    trade_detail = forms.CharField(label='交易详情', required=False)
    class Meta:
        model = Transactions
        fields = ('account', 'trade_money', 'trade_type', 'trade_detail')
    