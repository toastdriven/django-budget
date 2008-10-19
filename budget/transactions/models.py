import datetime
from decimal import Decimal
from django.db import models
from budget.categories.models import Category, StandardMetadata, ActiveManager


TRANSACTION_TYPES = (
    ('expense', 'Expense'),
    ('income', 'Income'),
)


class TransactionManager(ActiveManager):
    def get_latest(self, limit=10):
        return self.get_query_set().order_by('-date', '-created')[0:limit]


class TransactionExpenseManager(TransactionManager):
    def get_query_set(self):
        return super(TransactionExpenseManager, self).get_query_set().filter(transaction_type='expense')


class TransactionIncomeManager(TransactionManager):
    def get_query_set(self):
        return super(TransactionIncomeManager, self).get_query_set().filter(transaction_type='income')


class Transaction(StandardMetadata):
    """
    Represents incomes/expenses for the party doing the budgeting.
    
    Transactions are not tied to individual budgets because this allows
    different budgets to applied (like a filter) to a set of transactions.
    It also allows for budgets to change through time without altering the
    actual incoming/outgoing funds.
    """
    transaction_type = models.CharField(max_length=32, choices=TRANSACTION_TYPES, default='expense', db_index=True)
    notes = models.CharField(max_length=255, blank=True)
    category = models.ForeignKey(Category)
    amount = models.DecimalField(max_digits=11, decimal_places=2)
    date = models.DateField(default=datetime.date.today, db_index=True)
    
    objects = models.Manager()
    active = ActiveManager()
    expenses = TransactionExpenseManager()
    incomes = TransactionIncomeManager()
    
    def __unicode__(self):
        return u"%s (%s) - %s" % (self.notes, self.get_transaction_type_display(), self.amount)
    