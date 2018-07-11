from django.contrib import admin
from .models import Transaction, WL_Account
# Register your models here.

admin.site.register(Transaction)
admin.site.register(WL_Account)
