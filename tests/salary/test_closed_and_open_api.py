def test_is_open_property(factories):
    survey = factories.SurveyFactory(num_expected=5)
    survey.record_salary(10, key=5)
    survey.record_salary(10, key=3)
    survey.record_salary(10, key=7)
    survey.record_salary(10, key=13)

    assert survey.is_open
    assert not survey.is_finalized

    survey.finalize(10)

    assert not survey.is_open
    assert survey.is_finalized
