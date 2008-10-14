import datetime
from decimal import Decimal
from django.db import models


class StandardMetadata(models.Model):
    """
    A basic (abstract) model for metadata.
    """
    created = models.DateTimeField(default=datetime.datetime.now)
    updated = models.DateTimeField()
    is_deleted = models.BooleanField(default=False)
    
    class Meta:
        abstract = True
    
    def save(self, *args, **kwargs):
        self.updated = datetime.datetime.now()
        super(StandardMetadata, self).save(*args, **kwargs)
    
    def delete(self):
        self.is_deleted = True
        self.save()


class Category(StandardMetadata):
    name = models.CharField(max_length=128)
    slug = models.SlugField()
    
    class Meta:
        verbose_name_plural = 'Categories'
    
    def __unicode__(self):
        return self.name
    