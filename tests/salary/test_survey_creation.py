from django.core.urlresolvers import reverse

from disparity.apps.salary.utils import (
    unsign_survey_token,
)


def test_survey_creation_page(webtest_client, factories):
    url = reverse('survey-create')

    response = webtest_client.get(url)
    assert response.status_code == 200


def test_survey_creation(webtest_client, factories, models):
    url = reverse('survey-create')

    response = webtest_client.get(url)
    assert response.status_code == 200

    participant_emails = factories.EmailAddressFactory.create_batch(5)

    response.form['owner_email'] = 'owner@example.com'
    response.form['owner_salary'] = 12345
    response.form['participant_emails'] = ','.join(participant_emails)

    create_response = response.form.submit()

    assert create_response.status_code == 302

    detail_response = webtest_client.get(create_response.location)
    assert detail_response.status_code == 200

    token = detail_response.context['token']
    data = unsign_survey_token(token)
    survey = models.Survey.objects.get(uuid=data['survey_id'])
    assert survey.has_key_been_recorded(data['prime_identifier'])
    assert survey.total == data['seed'] + 12345
