import datetime
from decimal import Decimal
from django.db import models
from budget.categories.models import Category


class StandardMetadata(models.Model):
    """
    A basic (abstract) model for metadata.
    """
    created = models.DateTimeField(default=datetime.datetime.now)
    updated = models.DateTimeField()
    is_deleted = models.BooleanField(default=False)
    
    class Meta:
        abstract = True
    
    def save(self):
        self.updated = datetime.datetime.now()
        super(StandardMetadata, self).save()
    
    def delete(self):
        self.is_deleted = True
        self.save()


class Budget(StandardMetadata):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    start_date = models.DateTimeField(default=datetime.datetime.now)
    
    def __unicode__(self):
        return self.name
    
    def monthly_estimated_total(self):
        total = Decimal('0.0')
        for estimate in self.estimates.all():
            total += estimate.amount
        return total
    
    def yearly_estimated_total(self):
        return self.monthly_total() * 12


class BudgetEstimate(StandardMetadata):
    budget = models.ForeignKey(Budget, related_name='estimates')
    category = models.ForeignKey(Category, related_name='estimates')
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=11, decimal_places=2)
    
    def __unicode__(self):
        return u"%s - %s" % (self.name, self.amount)
    