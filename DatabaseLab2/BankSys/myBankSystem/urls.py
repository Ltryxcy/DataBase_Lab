from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'myBankSystem'
urlpatterns = [
    # 主页的URL
    path('', views.index, name='index'),
    # 部门视图的URL
    path('departments/', views.departments, name='departments'),
    path('department_staff/<int:department_id>/', views.department_staff, name='department_staff'),
    path('create_department/', views.create_department, name='create_department'),
    path('delete_department/<int:department_id>/', views.delete_department, name='delete_department'),
    path('edit_department/<int:department_id>/', views.edit_department, name='edit_department'),
    # 部门经理视图的URL
    path('set_manager/<int:staff_id>/<int:department_id>/', views.set_manager, name='set_manager'),
    path('delete_manager/<int:department_id>/', views.delete_manager, name='delete_manager'),
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
    path('create_trade/<int:account_id>/', views.create_trade, name='create_trade'),
    path('accounts_list/', views.accounts_list, name='accounts_list'),
    # 交易记录视图的URL
    path('transactions_info/<int:account_id>/', views.transactions_info, name='transactions_info'),
    path('transactions_list/', views.transactions_list, name='transactions_list'),
    # 支行视图的URL
    path('create_branch/', views.create_branch, name='create_branch'),
    path('branches/', views.branches, name='branches'),
    path('delete_branch/<str:branch_name>/', views.delete_branch, name='delete_branch'),
    path('edit_branch/<str:branch_name>/', views.edit_branch, name='edit_branch'),
    # 员工信息视图的URL
    path('create_staff/<int:department_id>/', views.create_staff, name='create_staff'),
    path('staff_list/', views.staff_list, name='staff_list'),
    path('edit_staff/<int:staff_id>/', views.edit_staff, name='edit_staff'),
    path('delete_staff/<int:staff_id>/', views.delete_staff, name='delete_staff'),
    # 贷款视图的URL
    path('apply_loan/<int:user_id>/<str:branch_name>/', views.apply_loan, name='apply_loan'),
    path('loans_info/<int:user_id>/', views.loans_info, name='loans_info'),
    path('repay_loan/<int:loan_id>/', views.repay_loan, name='repay_loan'),
    path('loans_list/', views.loans_list, name='loans_list')
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)