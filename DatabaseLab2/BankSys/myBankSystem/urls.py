from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

urlpatterns = [
    path('branches/', views.branches, name='branches'),
    path('departments/', views.departments, name='departments'),
    path('department_staff/<int:department_id>/', views.department_staff, name='department_staff'),
    path('login/', views.bank_user_login, name='login'),
]

urlpatterns += staticfiles_urlpatterns()