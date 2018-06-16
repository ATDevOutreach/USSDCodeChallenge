# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Account(models.Model):
    phonenumber= models.CharField(max_length=25,null=True)
    balance= models.DecimalField(null=True, default=0, max_digits=10, decimal_places=2)
    bank = models.CharField(max_length=25, null=True)
    bank_code = models.IntegerField(null=True)
    account_name = models.CharField(max_length=25, null=True)
    account_number = models.CharField(max_length=25, null=True)
    loan = models.DecimalField(null=True, default=0, max_digits=10, decimal_places=2)
    reg_date= models.DateField(auto_now_add=True)

    def __unicode__(self):
        return "{} with balance {}".format(self.phonenumber, self.balance)

    @classmethod
    def get_current_customer(cls, phonenumber):
        try:
            customer = cls.objects.get(phonenumber=phonenumber)
        except:
            customer = None
        return customer
    
    @classmethod
    def create_account(cls, phonenumber, sort_code=None, account_number=None, check_status=True):
        check = cls.objects.filter(phonenumber=phonenumber).exists()
        if check:
            return 'Account already exist. \n', False
        else:
            if not check_status:
                cls.objects.create(phonenumber=phonenumber)
                return 'Your phone number number has been successfully registerd', True
            return 'Does not exist', True

    def get_last_trans(self, **kwargs):
        if kwargs['status'] == Transaction.PENDING:
            trans = self.transaction.filter(status=Transaction.PENDING).last()
        else:
            trans = self.transaction.last()
        return trans
    
    def settle_loan(self):
        if self.balance > self.loan and self.loan > 0:
            self.balance -= self.loan
            self.loan = 0
            self.save()
            response = "END Loan Repaid was successful,\n"
            response += "New Balance: {}\n".format(self.balance)
            response += "Loan: {}".format(self.loan)
        elif self.loan == 0:
            response = "END You have no loan to pay back,\n"
            response += "Balance: {}\n".format(self.balance)
            response += "Loan: {}".format(self.loan)
        elif self.balance > 0 and self.loan > self.balance:
            self.loan -= self.balance
            self.balance = 0
            self.save()
            response = "END Loan Repaid was successful,\n"
            response += "New Balance: {}\n".format(self.balance)
            response += "Loan: {}".format(self.loan)
        else:
            response = "END You current balance can not settle your debt,\n"
            response += "Please Deposit in your account \n"
            response += "New Balance: {}\n".format(self.balance)
            response += "Loan: {}".format(self.loan)
        return response

class Transaction(models.Model):
    LOAN = 'loan'
    DEPOSIT = 'deposit'
    PENDING = 'pending'
    APPROVED = 'approved'
    CONCLUDED = 'concluded'
    PAYED = 'payed'
    NOT_PAYED = 'not_paid'
    DECLINED = 'declined'

    TRANSACTION_TYPES = (
        (LOAN, 'Loan'),
        (DEPOSIT, 'Deposit')
    )
    STATUS_TYPE = (
        (PENDING, 'Pending'),
        (CONCLUDED, 'Concluded'),
        (PAYED, 'Payed'),
        (NOT_PAYED, 'Not Payed'),
        (DECLINED, 'Declined'),
        (APPROVED, 'Approved')
    )
    trans_id = models.CharField(max_length=255, null=True, default='12345')
    status=models.CharField(max_length=30,null=True, choices=STATUS_TYPE)
    account = models.ForeignKey(Account, related_name="transaction")
    type = models.CharField(max_length=30, null=True, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(null=True, max_digits=10, decimal_places=2)
    date=models.DateField(auto_now_add=True)
    

    def __unicode__(self):
        return "{}".format(self.account.phonenumber)

    @classmethod
    def record(cls, **kwargs):
        if kwargs['type'] == cls.LOAN:
            cls.objects.create(
                account=kwargs['account'],
                type=kwargs['type'],
                status=kwargs['status'],
                amount=kwargs['amount']
            )
        elif kwargs['type'] == cls.DEPOSIT:
            cls.objects.create(
                account=kwargs['account'],
                type=kwargs['type'],
                trans_id=kwargs['trans_id'],
                status=kwargs['status'],
                amount=kwargs['amount']
            )
    
    @classmethod
    def check_loan_validity(cls, **kwargs):
        try:
            trans = cls.objects.get(trans_id=kwargs['access_code'], 
                account__phonenumber=kwargs['phonenumber'],
                status=cls.CONCLUDED)
        except:
            trans = False
        return trans

    def mark_as_paid(self, **kwargs):
        self.status = self.CONCLUDED
        self.save()
        self.account.balance += self.amount
        self.account.save()
        return self.account.balance, self.account.loan

    def received_loan(self, **kwargs):
        self.status = self.APPROVED
        self.save()
        self.account.loan += self.amount
        self.account.save()
        return self.account.balance, self.account.loan