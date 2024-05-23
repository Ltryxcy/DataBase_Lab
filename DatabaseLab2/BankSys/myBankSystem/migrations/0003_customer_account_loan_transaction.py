# Generated by Django 5.0.6 on 2024-05-22 16:25

import datetime
import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myBankSystem', '0002_bank_customer'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer_Account',
            fields=[
                ('account_id', models.AutoField(primary_key=True, serialize=False)),
                ('money', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='BranchAccount', to='myBankSystem.bank_branch')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='CustomerAccount', to='myBankSystem.bank_customer')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='CustomerAccount', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('loan_id', models.AutoField(primary_key=True, serialize=False)),
                ('loan_total', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('loan_deadline', models.DateTimeField(default=datetime.datetime(2027, 5, 23, 0, 25, 41, 309575))),
                ('loan_balance', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('loan_date', models.DateTimeField(auto_now_add=True)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='BranchLoan', to='myBankSystem.bank_branch')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Loan', to='myBankSystem.bank_customer')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('transaction_id', models.AutoField(primary_key=True, serialize=False)),
                ('money', models.FloatField(default=0.0)),
                ('transaction_type', models.CharField(choices=[('收入', '收入'), ('支出', '支出')], default='收入', max_length=100)),
                ('transaction_detail', models.CharField(blank=True, max_length=100)),
                ('transaction_date', models.DateTimeField(auto_now_add=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Transaction', to='myBankSystem.customer_account')),
            ],
        ),
    ]