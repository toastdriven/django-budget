import datetime
from decimal import Decimal
from django.db import models
from budget.categories.models import Category, StandardMetadata, ActiveManager


TRANSACTION_TYPES = (
    ('debit', 'Debit'),
    ('credit', 'Credit'),
)


class TransactionManager(ActiveManager):
    def get_latest(self, limit=10):
        return self.get_query_set().order_by('-date', '-created')[0:limit]


class TransactionDebitManager(TransactionManager):
    def get_query_set(self):
        return super(TransactionDebitManager, self).get_query_set().filter(transaction_type='debit')


class TransactionCreditManager(TransactionManager):
    def get_query_set(self):
        return super(TransactionCreditManager, self).get_query_set().filter(transaction_type='credit')


class Transaction(StandardMetadata):
    transaction_type = models.CharField(max_length=32, choices=TRANSACTION_TYPES, default='debit', db_index=True)
    notes = models.CharField(max_length=255, blank=True)
    category = models.ForeignKey(Category)
    amount = models.DecimalField(max_digits=11, decimal_places=2)
    date = models.DateField(default=datetime.date.today, db_index=True)
    
    objects = models.Manager()
    active = ActiveManager()
    debits = TransactionDebitManager()
    credits = TransactionCreditManager()
    
    def __unicode__(self):
        return u"%s (%s) - %s" % (self.notes, self.get_transaction_type_display(), self.amount)
    