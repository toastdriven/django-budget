import datetime
from decimal import Decimal
from django.db import models
from budget.models import StandardMetadata


class Category(StandardMetadata):
    name = models.CharField(max_length=128)
    slug = models.SlugField()
    
    class Meta:
        verbose_name_plural = 'Categories'
    
    def __unicode__(self):
        return self.name
    