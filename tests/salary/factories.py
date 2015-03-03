import factory

from django.utils import timezone

from disparity.apps.salary.utils import (
    generate_survey_token,
    SURVEY_TOKEN_MAX_AGE,
)
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


class TokenFactory(factory.Factory):
    seed = 12345
    prime_identifier = 5
    is_admin = False
    survey_id = 'survey-id'

    class Meta:
        model = staticmethod(generate_survey_token)
