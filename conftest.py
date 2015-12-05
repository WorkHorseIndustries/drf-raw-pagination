import pytest



@pytest.fixture()
def FooSerializer():
    from rest_framework import serializers
    from tests import models

    class FooSerializer(serializers.ModelSerializer):

        class Meta:
            model = models.Foo

    return FooSerializer



def pytest_configure():
    from django.conf import settings
    try:
        # setup from Django 1.7+
        from django import setup
    except ImportError:
        # Not needed in Django 1.6 or less
        setup = lambda: None

    settings.configure(
        DEBUG_PROPAGATE_EXCEPTIONS=True,
        DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3',
                               'NAME': ':memory:'}},
        SECRET_KEY='not very secret in tests',
        USE_I18N=True,
        USE_L10N=True,
        STATIC_URL='/static/',
        ROOT_URLCONF='tests.urls',
        MIDDLEWARE_CLASSES=(
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
        ),
        INSTALLED_APPS=(
            'django.contrib.auth',
            'django.contrib.contenttypes',

            'rest_framework',
            'tests',
        ),
        REST_FRAMEWORK={
            "TEST_REQUEST_DEFAULT_FORMAT": "json",
        },
    )
    setup()
