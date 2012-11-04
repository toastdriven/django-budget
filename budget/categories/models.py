import datetime
from decimal import Decimal
from django.db import models
from django.utils.translation import ugettext_lazy as _


class StandardMetadata(models.Model):
    """
    A basic (abstract) model for metadata.
    """
    created = models.DateTimeField(_('Created'), default=datetime.datetime.now)
    updated = models.DateTimeField(_('Updated'), default=datetime.datetime.now)
    is_deleted = models.BooleanField(_('Is deleted'), default=False, db_index=True)
    
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
    name = models.CharField(_('Name'), max_length=128)
    slug = models.SlugField(_('Slug'), unique=True)
    
    objects = models.Manager()
    active = ActiveManager()
    
    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
    
    def __unicode__(self):
        return self.name
    
