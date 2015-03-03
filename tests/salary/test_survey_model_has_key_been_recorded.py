def test_key_not_recorded(factories):
    survey = factories.SurveyFactory()
    survey.record_salary(10, 5)
    survey.record_salary(10, 13)
    survey.record_salary(10, 17)
    survey.record_salary(10, 19)

    assert not survey.has_key_been_recorded(23)

def test_key_has_been_recorded(factories):
    survey = factories.SurveyFactory()
    survey.record_salary(10, 5)
    survey.record_salary(10, 13)
    survey.record_salary(10, 17)
    survey.record_salary(10, 19)

    assert survey.has_key_been_recorded(5)
    assert survey.has_key_been_recorded(13)
    assert survey.has_key_been_recorded(17)
    assert survey.has_key_been_recorded(19)

def test_key_has_been_recorded_for_finalized_survey(factories):
    survey = factories.SurveyFactory()
    survey.record_salary(10, 5)
    survey.record_salary(10, 13)
    survey.record_salary(10, 17)
    survey.record_salary(10, 19)
    survey.finalize(1234)

    assert survey.has_key_been_recorded(5) is None
