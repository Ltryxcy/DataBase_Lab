from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views
app_name = 'myBankSystem'
urlpatterns = [
    path('', views.index, name='index'),
    path('branches/', views.branches, name='branches'),
    path('departments/', views.departments, name='departments'),
    path('department_staff/<int:department_id>/', views.department_staff, name='department_staff'),
    path('login/', views.bank_customer_login, name='login'),
    path('register/', views.bank_customer_register, name='register'),
    path('', include('django.contrib.auth.urls')),
]

urlpatterns += staticfiles_urlpatterns()