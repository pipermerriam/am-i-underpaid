import pytest


def test_survey_finalizing(factories):
    survey = factories.SurveyFactory(num_expected=5)

    seed = survey.total

    survey.record_salary(10, 5)
    survey.record_salary(20, 7)
    survey.record_salary(5, 11)
    survey.record_salary(5, 13)

    assert survey.is_open
    assert not survey.is_finalized

    assert survey.num_expected == 5
    assert survey.num_collected == 4

    survey.finalize(seed=seed)

    assert not survey.is_open
    assert survey.is_finalized
    assert survey.total == 10
    assert survey.num_collected is None
    assert survey.num_expected is None
    assert survey.tracker is None


def test_trying_to_finalize_unfinalizable_survey(factories):
    survey = factories.SurveyFactory(num_expected=5)

    seed = survey.total

    survey.record_salary(20, 7)
    survey.record_salary(5, 11)
    survey.record_salary(5, 13)

    with pytest.raises(ValueError):
        survey.finalize(seed)
