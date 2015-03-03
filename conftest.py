import pytest

from django_webtest import (
    WebTest,
)
@pytest.fixture()  # NOQA
def no_db_factories():
    import factory

    from tests.salary.factories import (  # NOQA
        EmailAddressFactory,
        TokenFactory,
    )

    def is_factory(obj):
        if not isinstance(obj, type):
            return False
        return issubclass(obj, factory.Factory)

    dict_ = {k: v for k, v in locals().items() if is_factory(v)}

    return type(
        'fixtures',
        (object,),
        dict_,
    )()


@pytest.fixture()  # NOQA
def factories(no_db_factories, transactional_db):
    import factory

    from tests.salary.factories import (  # NOQA
        SurveyFactory,
    )

    def is_factory(obj):
        if not isinstance(obj, type):
            return False
        return issubclass(obj, factory.Factory)

    dict_ = {k: v for k, v in locals().items() if is_factory(v)}

    return type(
        'fixtures',
        (no_db_factories.__class__,),
        dict_,
    )


@pytest.fixture()  # NOQA
def models(transactional_db):
    from django.apps import apps

    dict_ = {M._meta.object_name: M for M in apps.get_models()}

    return type(
        'models',
        (object,),
        dict_,
    )


@pytest.fixture()  # NOQA
def webtest_client(transactional_db):
    web_test = WebTest(methodName='__call__')
    web_test()
    return web_test.app
