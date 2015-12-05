import json
from django.core.urlresolvers import reverse
from tests.models import Foo
from tests.serializers import FooSerializer
from tests.views import FooViewSet
import pytest

pytestmark = pytest.mark.django_db

def test_empty_list(client):

    result = {
        'prev': '',
        'next': '',
        'count': 0,
        'results': []
    }

    resp = client.get(reverse('foo-list'))
    
    res = json.dumps(resp.content)
    for k in result.iterkeys():
        assert k in res
        assert res[k] == result[k]


def test_paginated_list(client):
    Foo.objects.bulk_create([Foo(name=str(i)) for i in xrange(20)])
    
    result = {
        'prev': '',
        'next': reverse('foo-list') + '?page_number=2',
        'count': '21',
        'results': [{'name': str(i), 'id': i+1} for i in xrange(9)]
    }

    resp = client.get(reverse('foo-list'))
    res = json.dumps(resp.content)

    for k in result.iterkeys():
        assert k in res
        assert res[k] == resutl[k]






