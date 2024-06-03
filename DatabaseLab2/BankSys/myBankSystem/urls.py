from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

app_name = 'myBankSystem'
urlpatterns = [
    path('', views.index, name='index'),
    path('branches/', views.branches, name='branches'),
    path('departments/', views.departments, name='departments'),
    path('department_staff/<int:department_id>/', views.department_staff, name='department_staff'),
    path('departments/create_department/', views.create_department, name='create_department'),
    # 用户视图的URL
    path('login/', views.bank_customer_login, name='login'),
    path('logout/', views.log_out, name='logout'),
    path('register/', views.bank_customer_register, name='register'),
    path('change_password/<int:user_id>/', views.change_password, name='change_password'),
    path('edition/<int:user_id>/', views.edit_customer, name='edition'),
    path('user_info/<int:user_id>/', views.user_info, name='user_info'),
    path('customers_info/', views.fetch_customers_information, name='customers_info'),
    path('delete_customer/<int:user_id>/', views.delete_customer, name='delete_customer'),
    # 账户视图的URL
    path('create_account/<int:user_id>/', views.create_account, name='create_account'),
    path('accounts_info/<int:user_id>/', views.accounts_info, name='accounts_info'),
    path('delete_account/<int:account_id>/', views.delete_account, name='delete_account'),
    path('trade/<int:account_id>/', views.trade, name='trade'),
    # 交易记录视图的URL
    path('transactions_info/<int:account_id>/', views.transactions_info, name='transactions_info'),
    # 支行视图的URL
    path('create_branch/', views.create_branch, name='create_branch'),
]
