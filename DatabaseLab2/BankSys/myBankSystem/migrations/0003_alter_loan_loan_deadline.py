# Generated by Django 5.0.6 on 2024-06-07 11:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myBankSystem', '0002_alter_loan_loan_deadline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='loan_deadline',
            field=models.DateTimeField(default=datetime.datetime(2027, 6, 7, 19, 1, 35, 94753)),
        ),
    ]