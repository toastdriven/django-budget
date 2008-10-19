import datetime
from decimal import Decimal
from django.db import models


class StandardMetadata(models.Model):
    """
    A basic (abstract) model for metadata.
    """
    created = models.DateTimeField(default=datetime.datetime.now)
    updated = models.DateTimeField()
    is_deleted = models.BooleanField(default=False, db_index=True)
    
    class Meta:
        abstract = True
    
    def save(self, *args, **kwargs):
        self.updated = datetime.datetime.now()
        super(StandardMetadata, self).save(*args, **kwargs)
    
    def delete(self):
        self.is_deleted = True
        self.save()


class ActiveManager(models.Manager):
    def get_query_set(self):
        return super(ActiveManager, self).get_query_set().filter(is_deleted=False)


class Category(StandardMetadata):
    """
    Categories are the means to loosely tie together the transactions and
    estimates.
    
    They are used to aggregate transactions together and compare them to the
    appropriate budget estimate. For the reasoning behind this, the docstring
    on the Transaction object explains this.
    """
    name = models.CharField(max_length=128)
    slug = models.SlugField(unique=True)
    
    objects = models.Manager()
    active = ActiveManager()
    
    class Meta:
        verbose_name_plural = 'Categories'
    
    def __unicode__(self):
        return self.name
    