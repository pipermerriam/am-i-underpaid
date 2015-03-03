from django.core.urlresolvers import reverse


def test_survey_detail_page_without(webtest_client, factories):
    survey = factories.SurveyFactory(num_collected=3, _tracker=str(5 * 7 * 13))

    token = factories.TokenFactory(
        is_admin=True,
        prime_identifier=17,
        survey_id=survey.uuid,
    )
    url = reverse('survey-detail', kwargs={'token': token})

    response = webtest_client.get(url)

    assert 'survey-finalize' not in response.forms


def test_survey_detail_page_with_finalize_form(webtest_client, factories):
    survey = factories.SurveyFactory(num_collected=4, _tracker=str(5 * 7 * 13 * 17))

    token = factories.TokenFactory(
        is_admin=True,
        prime_identifier=17,
        survey_id=survey.uuid,
    )
    url = reverse('survey-detail', kwargs={'token': token})

    response = webtest_client.get(url)

    assert 'survey-finalize' in response.forms


def test_finalizing_a_survey_manually(webtest_client, factories, models):
    survey = factories.SurveyFactory(
        num_collected=4, num_expected=10, _tracker=str(5 * 7 * 13 * 17),
    )

    token = factories.TokenFactory(
        is_admin=True,
        prime_identifier=17,
        survey_id=survey.uuid,
    )
    url = reverse('survey-detail', kwargs={'token': token})

    response = webtest_client.get(url)

    finalize_response = response.forms['survey-finalize'].submit()
    assert finalize_response.status_code == 302
    assert finalize_response.location.endswith(url)

    updated_survey = models.Survey.objects.get(pk=survey.pk)
    assert updated_survey.is_finalized


def test_finalizing_as_non_admin(client, factories, models):
    survey = factories.SurveyFactory(
        num_collected=4, num_expected=10, _tracker=str(5 * 7 * 13 * 17),
    )

    token = factories.TokenFactory(
        is_admin=False,
        prime_identifier=17,
        survey_id=survey.uuid,
    )
    url = reverse('survey-finalize', kwargs={'token': token})

    response = client.post(url)
    assert response.status_code == 404


def test_finalizing_to_early(client, factories, models):
    survey = factories.SurveyFactory(
        num_collected=3, num_expected=10, _tracker=str(5 * 7 * 13),
    )

    token = factories.TokenFactory(
        is_admin=True,
        prime_identifier=17,
        survey_id=survey.uuid,
    )
    url = reverse('survey-finalize', kwargs={'token': token})

    response = client.post(url)
    assert response.status_code == 404
