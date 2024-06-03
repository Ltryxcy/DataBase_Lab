from django.contrib import admin
from .models import Bank_Branch, Bank_Department, Bank_Staff, Department_Manager
from .models import Bank_Customer, Customer_Account, Transactions, Loan
# Register your models here.

admin.site.register(Bank_Branch)
admin.site.register(Bank_Department)
admin.site.register(Bank_Staff)
admin.site.register(Department_Manager)
admin.site.register(Bank_Customer)
admin.site.register(Customer_Account)
admin.site.register(Transactions)
admin.site.register(Loan)