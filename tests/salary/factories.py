import factory

from disparity.apps.salary.models import (
    Survey,
)


class EmailAddressFactory(factory.Factory):
    value = factory.Sequence("test-{0}@example.com".format)

    class Meta:
        model = str
        inline_args = ("value",)


class SurveyFactory(factory.DjangoModelFactory):
    num_expected = 5

    class Meta:
        model = Survey
