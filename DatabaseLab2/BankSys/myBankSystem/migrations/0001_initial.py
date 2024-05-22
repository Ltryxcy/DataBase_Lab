# Generated by Django 5.0.6 on 2024-05-22 06:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bank_Branch',
            fields=[
                ('branch_name', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('branch_city', models.CharField(max_length=30)),
                ('branch_tel', models.CharField(max_length=11)),
                ('branch_manager', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Bank_Department',
            fields=[
                ('department_id', models.AutoField(primary_key=True, serialize=False)),
                ('department_name', models.CharField(max_length=30)),
                ('department_manager', models.CharField(max_length=20)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Bank_department', to='myBankSystem.bank_branch')),
            ],
        ),
        migrations.CreateModel(
            name='Bank_Staff',
            fields=[
                ('staff_id', models.AutoField(primary_key=True, serialize=False)),
                ('staff_photo', models.ImageField(default='photos/GGbond.jpg', upload_to='photos/%Y%m%d/')),
                ('staff_name', models.CharField(max_length=20)),
                ('staff_sex', models.CharField(max_length=10)),
                ('staff_tel', models.CharField(max_length=11)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='DepartmentStaff', to='myBankSystem.bank_department')),
            ],
        ),
        migrations.CreateModel(
            name='Branch_Manager',
            fields=[
                ('bank_staff_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='myBankSystem.bank_staff')),
                ('branch_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='BranchManager', to='myBankSystem.bank_branch')),
            ],
            bases=('myBankSystem.bank_staff',),
        ),
        migrations.CreateModel(
            name='Department_Manager',
            fields=[
                ('bank_staff_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='myBankSystem.bank_staff')),
                ('dept_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='DepartmentManager', to='myBankSystem.bank_department')),
            ],
            bases=('myBankSystem.bank_staff',),
        ),
    ]
