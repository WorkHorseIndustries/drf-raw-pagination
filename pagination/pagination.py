from .paginator import RawablPagNumberPaginator
from .db.models.query import PaginatedRawQuerySet
from django.core.paginator import Paginator as DjangoPaginator
from rest_framework.pagination import PageNumberPagination


class RawablePageNumberPaginator(PageNumberPagination):
    
    def paginate_queryset(self, queryset, request, view=None):
        if isinstance(queryset, PaginatedRawQuerySet):
            # really wish he hadn't named this the way he did.
            self.django_paginator_class = RawPaginator
        else:
            self.django_paginator_class = DjangoPaginator

        return super(RawablePageNumberPaginator, self).paginate_queryset(queryset, request, view)

