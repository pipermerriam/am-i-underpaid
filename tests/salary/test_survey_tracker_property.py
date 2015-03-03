import operator

from disparity.apps.salary.utils import (
    PRIMES,
)


def test_tracker_getting(factories):
    survey = factories.SurveyFactory()

    survey.tracker = 12345L

    assert survey._tracker == '12345'
    assert survey.tracker == 12345L


def test_tracker_setting_with_huge_number(factories, models):
    huge_number = reduce(operator.mul, PRIMES)

    survey = factories.SurveyFactory()
    survey.tracker = huge_number
    survey.save()

    updated_survey = models.Survey.objects.get(pk=survey.pk)
    assert updated_survey.tracker == huge_number


def test_setting_and_getting_null(factories):
    survey = factories.SurveyFactory()
    survey.tracker = None
    assert survey._tracker is None
    assert survey.tracker is None
