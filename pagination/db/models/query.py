from django.db import connection
from django.db.models import sql
from django.db.models.query import RawQuerySet

class PaginatedRawQuerySet(RawQuerySet):

    _count = None
    
    def __init__(self, raw_query, *args, **kwargs):
        
        self._query = raw_query
        super(PaginatedRawQuerySet, self).__init__(raw_query, *args, **kwargs)

    def page(self, limit, offset):
        self.query = sql.RawQuery(self._query + 'LIMIT %(limit)s OFFSET %(offset)s', using=self.db, params=self.params)

    def count(self):
        if self._count == None:
            q = 'SELECT COUNT(*) FROM (' + self._query + ') b;' 
            cursor = connection.cursor()
            cursor.execute(q, self.params)
            row = cursor.fetchone()
            self._count = row [0]
        return self._count


    def __len__(self):
        return self.count()

    def __repr__(self):
        return "<PaginatedRawQuerySet: %s>" % self.query


