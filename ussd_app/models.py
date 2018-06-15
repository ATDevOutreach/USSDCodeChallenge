# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Account(models.Model):
    phonenumber= models.CharField(max_length=25,null=True)
    balance= models.IntegerField(null=True)
    loan= models.IntegerField(null=True)
    reg_date= models.DateField(auto_now_add=True)

    def __unicode__(self):
        return "{} with balance {}".format(self.phonenumber, self.balance)

# class Coperative(models.Model):
#     name = models.CharField(max_length=30,null=True)
#     phonenumber = models.CharField(max_length=20,null=True)
#     city = models.CharField(max_length=30,null=True)
#     reg_date=models.DateField(auto_now_add=True)
#     level = models.IntegerField(null=True)

class Transaction(models.Model):
    status=models.CharField(max_length=30,null=True)
    account = models.ForeignKey(Account)
    type = models.CharField(max_length=30, null=True)
    amount = models.IntegerField(null=True)
    date=models.DateField(auto_now_add=True)

    def __unicode__(self):
        return "{}".format(self.account.phonenumber)
