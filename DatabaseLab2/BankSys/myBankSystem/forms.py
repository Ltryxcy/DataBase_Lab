from django import forms
from django.contrib.auth.models import User
from .models import Bank_Customer, Customer_Account, Bank_Staff, Bank_Branch

# 登录只有用户名和密码两个字段
class BankCustomer_LoginForm(forms.Form):
    username = forms.CharField(label='用户名', strip=True, error_messages={'required': '用户名不能为空。'})
    # 密码字段，允许空格，输入时隐藏密码
    password = forms.CharField(label='密码', strip=False, error_messages={'required': '密码不能为空。'}, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password')
#   注册表单,包含身份证号，姓名，电话号码，邮箱，名下账户数       
class BankCustomer_RegisterForm(forms.Form):
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
class BankCustomer_EditForm(forms.Form):
    # 不能修改身份证号
    id = forms.CharField(label='身份证号', strip=True, disabled=True)
    # 姓名不能为空
    name = forms.CharField(label='姓名', strip=True, error_messages={'required': '姓名不能为空。'})
    # 电话号码不能为空
    tel = forms.CharField(label='电话号码', strip=True, error_messages={'required': '电话号码不能为空。'})
    # 邮箱可以为空
    email = forms.EmailField(label='邮箱', required=False)
    # 名下账户数不能修改
    account_cnt = forms.IntegerField(label='名下账户数', disabled=True)
    class meta:
        model = Bank_Customer
        fields = ('id', 'name', 'tel', 'email', 'account_cnt')