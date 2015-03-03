from django.core.urlresolvers import reverse


def test_survey_salary_recording(webtest_client, factories, models):
    survey = factories.SurveyFactory(num_collected=3, _tracker=str(5 * 7 * 13))
    seed = survey.total

    token = factories.TokenFactory(
        prime_identifier=17,
        survey_id=survey.uuid,
    )
    url = reverse('survey-detail', kwargs={'token': token})

    response = webtest_client.get(url)

    assert 'record-salary' in response.forms
    response.forms['record-salary']['salary'] = 12345

    salary_response = response.forms['record-salary'].submit()
    assert salary_response.status_code == 302
    assert salary_response.location.endswith(url)

    updated_survey = models.Survey.objects.get(pk=survey.pk)
    assert updated_survey.total == seed + 12345


def test_survey_auto_finalizes_on_last_response(webtest_client, factories, models):
    survey = factories.SurveyFactory(
        num_collected=4, num_expected=5, _tracker=str(5 * 7 * 13 * 17))
    seed = survey.total

    token = factories.TokenFactory(
        prime_identifier=23,
        survey_id=survey.uuid,
    )
    url = reverse('survey-detail', kwargs={'token': token})

    response = webtest_client.get(url)

    assert 'record-salary' in response.forms
    response.forms['record-salary']['salary'] = 12345

    salary_response = response.forms['record-salary'].submit()
    assert salary_response.status_code == 302
    assert salary_response.location.endswith(url)

    updated_survey = models.Survey.objects.get(pk=survey.pk)
    assert updated_survey.is_finalized
