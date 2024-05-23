from django.contrib import admin
from .models import Bank_Branch, Bank_Department, Bank_Staff, Branch_Manager, Department_Manager
from .models import Bank_Customer, Customer_Account, Transaction, Loan
# Register your models here.

admin.site.register(Bank_Branch)
admin.site.register(Bank_Department)
admin.site.register(Bank_Staff)
admin.site.register(Branch_Manager)
admin.site.register(Department_Manager)
admin.site.register(Bank_Customer)
admin.site.register(Customer_Account)
admin.site.register(Transaction)
admin.site.register(Loan)