# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-15 16:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ussd_app', '0004_auto_20180615_1518'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='trans_id',
            field=models.CharField(default=1234, max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('concluded', 'Concluded')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='type',
            field=models.CharField(choices=[('loan', 'Loan'), ('deposit', 'Deposit')], max_length=30, null=True),
        ),
    ]
