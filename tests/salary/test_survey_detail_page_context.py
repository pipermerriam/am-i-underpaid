from django.core.urlresolvers import reverse


def test_survey_detail_page_with_admin_token(client, factories):
    survey = factories.SurveyFactory(num_collected=3, _tracker=str(5 * 7 * 13))

    token = factories.TokenFactory(
        is_admin=True,
        survey_id=survey.uuid,
        prime_identifier=17,
    )
    url = reverse('survey-detail', kwargs={'token': token})

    response = client.get(url)
    assert response.status_code == 200

    assert 'is_admin' in response.context
    assert response.context['is_admin'] is True


def test_survey_detail_page_with_regular(client, factories):
    survey = factories.SurveyFactory(num_collected=3, _tracker=str(5 * 7 * 13))

    token = factories.TokenFactory(
        prime_identifier=17,
        survey_id=survey.uuid,
    )
    url = reverse('survey-detail', kwargs={'token': token})

    response = client.get(url)
    assert response.status_code == 200

    assert 'is_admin' in response.context
    assert response.context['is_admin'] is False


def test_survey_detail_page_with_unsubmitted_key(client, factories):
    survey = factories.SurveyFactory(num_collected=3, _tracker=str(5 * 7 * 13))

    token = factories.TokenFactory(
        prime_identifier=17,
        survey_id=survey.uuid,
    )
    url = reverse('survey-detail', kwargs={'token': token})

    response = client.get(url)
    assert response.status_code == 200

    assert 'key_has_been_submitted' in response.context
    assert response.context['key_has_been_submitted'] is False


def test_survey_detail_page_with_already_submitted_key(client, factories):
    survey = factories.SurveyFactory(num_collected=3, _tracker=str(5 * 7 * 13 * 17))

    token = factories.TokenFactory(
        prime_identifier=17,
        survey_id=survey.uuid,
    )
    url = reverse('survey-detail', kwargs={'token': token})

    response = client.get(url)
    assert response.status_code == 200

    assert 'key_has_been_submitted' in response.context
    assert response.context['key_has_been_submitted'] is True


def test_survey_detail_page_finalized_survey(client, factories):
    survey = factories.SurveyFactory(num_collected=4, _tracker=str(5 * 7 * 13 * 17))
    survey.finalize(12345)

    token = factories.TokenFactory(
        is_admin=False,
        prime_identifier=17,
        survey_id=survey.uuid,
    )
    url = reverse('survey-detail', kwargs={'token': token})

    response = client.get(url)
    assert response.status_code == 200

    assert 'key_has_been_submitted' in response.context
    assert response.context['key_has_been_submitted'] is None
