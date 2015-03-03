import pytest

from django.core import mail
from django.core.urlresolvers import reverse

from disparity.apps.salary.emails import (
    send_survey_creation_email,
)


@pytest.mark.django_db
def test_sending_survey_creation_email(factories):
    assert len(mail.outbox) == 0

    all_emails=factories.EmailAddressFactory.create_batch(5)
    token = factories.TokenFactory(
        prime_identifier=5,
        survey_id='some-id',
    )
    detail_url = reverse('survey-detail', kwargs={'token': token})
    send_survey_creation_email(
        email='test@example.com',
        all_emails=all_emails,
        token=token,
    )
    assert len(mail.outbox) == 1
    message = mail.outbox[0]
    assert detail_url in message.body
    assert all(
        [email in message.body for email in all_emails]
    )
