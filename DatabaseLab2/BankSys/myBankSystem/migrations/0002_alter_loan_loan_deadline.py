# Generated by Django 5.0.6 on 2024-06-02 03:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myBankSystem', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='loan_deadline',
            field=models.DateTimeField(default=datetime.datetime(2027, 6, 2, 11, 55, 25, 551824)),
        ),
    ]