# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from . import models
# Register your models here.

class AccountAdmin(admin.ModelAdmin):
    list_display = ['phonenumber', 'balance', 'loan']
admin.site.register(models.Account, AccountAdmin)

class TransactionAdmin(admin.ModelAdmin):
    list_display = ['account', 'type', 'amount', 'status', 'trans_id']
admin.site.register(models.Transaction, TransactionAdmin)
