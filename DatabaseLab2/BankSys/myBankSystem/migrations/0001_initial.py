# Generated by Django 5.0.6 on 2024-06-03 16:31

import datetime
import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bank_Branch',
            fields=[
                ('branch_name', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('branch_city', models.CharField(max_length=30)),
                ('branch_tel', models.CharField(max_length=11)),
            ],
        ),
        migrations.CreateModel(
            name='Bank_Customer',
            fields=[
                ('id', models.CharField(max_length=18, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=20)),
                ('tel', models.CharField(max_length=11)),
                ('email', models.EmailField(blank=True, max_length=50)),
                ('accounts_cnt', models.IntegerField(default=0)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='BankCustomer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Bank_Department',
            fields=[
                ('department_id', models.AutoField(primary_key=True, serialize=False)),
                ('department_name', models.CharField(max_length=30)),
                ('department_manager', models.CharField(blank=True, max_length=20, null=True)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Bank_department', to='myBankSystem.bank_branch')),
            ],
        ),
        migrations.CreateModel(
            name='Bank_Staff',
            fields=[
                ('staff_id', models.AutoField(primary_key=True, serialize=False)),
                ('staff_photo', models.ImageField(default='photos/default.jpg', upload_to='photos/%Y%m%d/')),
                ('staff_name', models.CharField(max_length=20)),
                ('staff_sex', models.CharField(max_length=10)),
                ('staff_tel', models.CharField(max_length=11)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='DepartmentStaff', to='myBankSystem.bank_department')),
            ],
        ),
        migrations.CreateModel(
            name='Customer_Account',
            fields=[
                ('account_id', models.AutoField(primary_key=True, serialize=False)),
                ('money', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='BranchAccount', to='myBankSystem.bank_branch')),
                ('user', models.ForeignKey(default='0', on_delete=django.db.models.deletion.CASCADE, related_name='CustomerAccount', to='myBankSystem.bank_customer')),
            ],
        ),
        migrations.CreateModel(
            name='Department_Manager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departments', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departments_manager', to='myBankSystem.bank_department')),
                ('staffs', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='staffs_manager', to='myBankSystem.bank_staff')),
            ],
        ),
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('loan_id', models.AutoField(primary_key=True, serialize=False)),
                ('loan_total', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('loan_deadline', models.DateTimeField(default=datetime.datetime(2027, 6, 4, 0, 31, 31, 723836))),
                ('loan_balance', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('loan_date', models.DateTimeField(auto_now_add=True)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='BranchLoan', to='myBankSystem.bank_branch')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Loan', to='myBankSystem.bank_customer')),
            ],
        ),
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('transaction_id', models.AutoField(primary_key=True, serialize=False)),
                ('money', models.FloatField(default=0.0)),
                ('transaction_type', models.CharField(choices=[('收入', '收入'), ('支出', '支出')], default='支出', max_length=100)),
                ('transaction_detail', models.CharField(blank=True, max_length=100)),
                ('transaction_date', models.DateTimeField(auto_now_add=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Transactions', to='myBankSystem.customer_account')),
            ],
        ),
    ]
