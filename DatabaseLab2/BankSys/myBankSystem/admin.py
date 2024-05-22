from django.contrib import admin
from .models import Bank_Branch, Bank_Department, Bank_Staff, Branch_Manager, Department_Manager
# Register your models here.

admin.site.register(Bank_Branch)
admin.site.register(Bank_Department)