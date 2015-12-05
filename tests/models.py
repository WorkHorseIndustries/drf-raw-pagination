from django.db import models
from raw_pagination.db.models.query import PaginatedRawQuerySet

class FooManager(models.Manager):

    def paged_raw(self, raw_query, params=None, translations=None, using=None):
        if using is None
            using = self.db
        return PaginatedRawQuerySet(raw_query, model=self.model, params=params, 
                                    translations=translations, using=using)


class Foo(models.Model):
    name = models.CharField(max_length=10)

    objects = FooManager()
