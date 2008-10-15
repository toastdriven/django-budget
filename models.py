import datetime
from decimal import Decimal
from django.db import models
from budget.categories.models import Category, StandardMetadata, ActiveManager
from budget.transactions.models import Transaction


class BudgetManager(ActiveManager):
    def most_current_for_date(self, date):
        return super(BudgetManager, self).get_query_set().filter(start_date__lte=date).latest('start_date')


class Budget(StandardMetadata):
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


class BudgetEstimate(StandardMetadata):
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
        return Transaction.active.filter(category=self.category, date__gte=start_date, date__lte=end_date)
    
    def actual_amount(self, start_date, end_date):
        total = Decimal('0.0')
        for transaction in self.actual_transactions(start_date, end_date):
            total += transaction.amount
        return total
        
    