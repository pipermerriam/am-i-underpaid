import pytest


def test_record_salary(factories, models):
    survey = factories.SurveyFactory()
    total = survey.total

    survey.record_salary(10, key=5)

    updated_survey = models.Survey.objects.get(pk=survey.pk)
    assert updated_survey.total == total + 10


def test_cannot_record_salary_twice(factories):
    survey = factories.SurveyFactory()

    survey.record_salary(10, key=5)
    with pytest.raises(ValueError):
        survey.record_salary(10, key=5)


def test_multiple_response_restriction_with_many_keys(factories):
    survey = factories.SurveyFactory()

    survey.record_salary(10, key=5)
    survey.record_salary(10, key=11)
    survey.record_salary(10, key=13)
    survey.record_salary(10, key=23)

    with pytest.raises(ValueError):
        survey.record_salary(10, key=5)
