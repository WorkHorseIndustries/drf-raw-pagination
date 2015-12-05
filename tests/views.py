from rest_framework import viewsets 
from rest_framework.mixins import ListModelMixin
from .serializers import FooSerializer
from .models import Foo
from raw_pagination.pagination import RawablePageNumberPagination


class FooViewSet(ListModelMixin, viewsets.GenericViewSet):
    serializer_class = FooSerializer
    pagination_class = RawablePageNumberPagination
    queryset = Foo.objects.all()

    def get_queryset(self):
        Foo.objects.paged_raw("SELECT * FROM foo_foo")
