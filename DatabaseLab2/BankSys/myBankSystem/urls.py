from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

app_name = 'myBankSystem'
urlpatterns = [
    path('branches/', views.branches, name='branches'),
    path('departments/', views.departments, name='departments'),
    path('department_staff/<int:department_id>/', views.department_staff, name='department_staff'),
    # 用户视图的URL
    path('login/', views.bank_customer_login, name='login'),
    path('logout/', views.log_out, name='logout'),
    path('register/', views.bank_customer_register, name='register'),
    path('', include('django.contrib.auth.urls')),
    path('change_password/<int:customer_id>/', views.change_password, name='change_password'),
    path('edition/<int:customer_id>/', views.edit_customer, name='edition'),
    path('fetch_customers/', views.fetch_customers_information, name='fetch_customers'),
    # 账户视图的URL
    path('create_account/<int:customer_id>/<str:branch_name>/', views.create_account, name='create_account'),
    path('accounts_info/<int:customer_id>/', views.accounts_info, name='accounts_info'),
    path('delete_account/<int:account_id>/', views.delete_account, name='delete_account'),
    # path('trade/<int:account_id>/', views.trade, name='trade'),
]

urlpatterns += staticfiles_urlpatterns()