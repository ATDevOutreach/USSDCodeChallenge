from django.db import models

# Create your models here.
class WL_Account(models.Model):
    phone_number = models.CharField(max_length=25)
    #credit
    balance = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    #owing
    debt = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    bank_name = models.CharField(max_length=30, blank=True)
    bank_code = models.IntegerField(null=True)
    account_name = models.CharField(max_length=60, blank=True)
    account_number = models.CharField(max_length=10, blank=True)
    reg_data = models.DateField(auto_now_add=True)

    @classmethod
    def get_wl_account(cls, phone_number):
        try:
            customer = cls.objects.get(phone_number=phone_number)
        except:
            customer = None
        return customer

    def get_last_transaction(self, status):
        if status == Transaction.PENDING:
            transaction_instance = self.transactions.filter(status=Transaction.PENDING).last()
        else:
            transaction_instance = self.transaction.last()
        return transaction_instance

    def repay_debts(self):
        if self.balance > self.debt:
            self.balance -= self.debt
            self.debt = 0
            self.save()
            return "END your debt has been successfully cleared"
        
        if self.debt == 0:
            return "END You don't have any outstanding debts"
        
        if self.balance < self.debt:
            return "END You don't have sufficient money to repay your loan. Try depositing money"

    def __str__(self):
        return "{}".format(self.phone_number)

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

    transaction_id = models.CharField(max_length=255)
    status=models.CharField(max_length=30,null=True, choices=STATUS_TYPE)
    type = models.CharField(max_length=30, null=True, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(null=True, max_digits=10, decimal_places=2)
    transaction_fee = models.DecimalField(null=True, max_digits=10, decimal_places=2)
    date=models.DateField(auto_now_add=True)
    account = models.ForeignKey(WL_Account, related_name="transactions")
    
    def mark_as_paid(self, **kwargs):
        self.status = self.CONCLUDED
        self.save()
        self.account.balance += self.amount
        self.account.save()
        return self.account.balance

    def update_debt_balance(self, amount):
        self.account.debt += amount
        self.account.save()