import datetime
from decimal import Decimal
from django.db import models
from budget.models import StandardMetadata
from budget.categories.models import Category


TRANSACTION_TYPES = (
    ('debit', 'Debit'),
    ('credit', 'Credit'),
)


class TransactionManager(models.Manager):
    pass


class Transaction(StandardMetadata):
    transaction_type = models.CharField(max_length=32, choices=TRANSACTION_TYPES, default='debit')
    name = models.CharField(max_length=255, blank=True)
    category = models.ForeignKey(Category, blank=True, null=True)
    amount = models.DecimalField(max_digits=11, decimal_places=2)
    date = models.DateTimeField(default=datetime.datetime.now)
    
    objects = models.Manager()
    # debits = TransactionDebitManager()
    # credits = TransactionCreditManager()
    
    def __unicode__(self):
        return u"%s (%s) - %s" % (self.name, self.get_transaction_type_display(), self.amount)
    