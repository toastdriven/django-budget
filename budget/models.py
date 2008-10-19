import datetime
from decimal import Decimal
from django.db import models
from budget.categories.models import Category, StandardMetadata, ActiveManager
from budget.transactions.models import Transaction


class BudgetManager(ActiveManager):
    def most_current_for_date(self, date):
        return super(BudgetManager, self).get_query_set().filter(start_date__lte=date).latest('start_date')


class Budget(StandardMetadata):
    """
    An object representing a budget.
    
    Only estimates are tied to a budget object, which allows different budgets
    to be applied to the same set of transactions for comparision.
    """
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    start_date = models.DateTimeField(default=datetime.datetime.now, db_index=True)
    
    objects = models.Manager()
    active = BudgetManager()
    
    def __unicode__(self):
        return self.name
    
    def monthly_estimated_total(self):
        total = Decimal('0.0')
        for estimate in self.estimates.all():
            total += estimate.amount
        return total
    
    def yearly_estimated_total(self):
        return self.monthly_estimated_total() * 12
    
    def estimates_and_transactions(self, start_date, end_date):
        estimates_and_transactions = []
        actual_total = Decimal('0.0')

        for estimate in self.estimates.all():
            actual_amount = estimate.actual_amount(start_date, end_date)
            actual_total += actual_amount
            estimates_and_transactions.append({
                'estimate': estimate,
                'transactions': estimate.actual_transactions(start_date, end_date),
                'actual_amount': actual_amount,
            })
        
        return (estimates_and_transactions, actual_total)
    
    def actual_total(self, start_date, end_date):
        actual_total = Decimal('0.0')

        for estimate in self.estimates.all():
            actual_amount = estimate.actual_amount(start_date, end_date)
            actual_total += actual_amount
        
        return actual_total


class BudgetEstimate(StandardMetadata):
    """
    The individual line items that make up a budget.
    
    Some examples include possible items like "Mortgage", "Rent", "Food", "Misc"
    and "Car Payment".
    """
    budget = models.ForeignKey(Budget, related_name='estimates')
    category = models.ForeignKey(Category, related_name='estimates')
    amount = models.DecimalField(max_digits=11, decimal_places=2)
    
    objects = models.Manager()
    active = ActiveManager()
    
    def __unicode__(self):
        return u"%s - %s" % (self.category.name, self.amount)
    
    def yearly_estimated_amount(self):
        return self.amount * 12
    
    def actual_transactions(self, start_date, end_date):
        # Estimates should only report on expenses to prevent incomes from 
        # (incorrectly) artificially inflating totals.
        return Transaction.expenses.filter(category=self.category, date__range=(start_date, end_date)).order_by('date')
    
    def actual_amount(self, start_date, end_date):
        total = Decimal('0.0')
        for transaction in self.actual_transactions(start_date, end_date):
            total += transaction.amount
        return total
        
    