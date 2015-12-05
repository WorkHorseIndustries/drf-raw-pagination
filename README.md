#drf-raw-pagination

Provides pagination for Django's RawQuerySet.  The original intention was for this to be used with [django-rest-framework](http://www.django-rest-framework.org/).

There are three different components involved, the PaginatedRawQuerySet, the Paginator, and Pagination class. 

##PaginatedRawQuerySet
`PaginatedRawQuery` is a subclass of RawQuerySet, extending it with `count`, and `page` methods.

`count` will hit the Database the first time it's called, and return the total count of all records matching the query

```python
    PaginatedRawQuery("SELECT * FROM foo_bar")
```
`count()` will execute 
```sql
    SELECT COUNT(*) FROM (SELECT * FROM foo_bar) b;
```
and cache the result so future calls to count wont hit the database. 


`page` takes two parameters `limit` and `offset` which are used by there respective SQL expressions
to return a paged result set. 

```python
    PaginatedRawQuery("SELECT * FROM foo_bar")
```
`page(2, 3)` will execute

```sql
    SELECT * FROM foo_bar LIMIT 2 OFFSET 3
```

##Paginator
`RawPaginator` and `RawPage` implements the [Paginator and Page contracts](https://docs.djangoproject.com/en/1.9/topics/pagination/) specified by Django. They rely on the `count` and `page` being implemented by the underlying queryset. 

##Pagination
`RawablePageNumberPaginator` extends DRF's `PageNumberPaginator`, it checks whether the queryset is an instance of `PaginatedRawQuerySet` and if so, it uses the `RawPaginator` otherwise it uses the default `DjangoPaginator`.


##Example
models.py
```
from djang.db import models
from .managers import FooManager

class Foo(models.Model):
    name = model.CharField(max_length=10)

    objects = FooManager()

```


manage.py

```python
from django.db import models
from raw_pagination.db.models.query import PaginatedRawQuerySet

class FooManager(models.Manager):

    def paged_raw(self, raw_query, params=None, translations=None, using=None):
        if using is None
            using = self.db
        return PaginatedRawQuerySet(raw_query, model=self.model, params=params, 
                                    translations=translations, using=using)

```

serializers.py
```python
from rest_framework import serializers
from .models import Foo

class FooSerializer(serializers.ModelSerializer):

    class Meta:
        model = Foo
        fields = ('name')

```


api.py
```python
from rest_framework import generics
from rest_framework.mixins import ListModelMixin
from .serializers import FooSerializer
from .models import Foo
from raw_pagination.pagination import RawablePageNumberPagination


class FooView(ListModelMixin, generics.GenericView):
    serializer_class = FooSerializer
    pagination_class = RawablePageNumberPagination

    def get_queryset(self):
        Foo.objects.paged_raw("SELECT * FROM foo_foo")
        
```
