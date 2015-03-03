from emailtools import mixins

from django.utils import timezone
from django.core.urlresolvers import reverse

from disparity.apps.core.emails import DisparityEmail
from disparity.apps.salary.utils import SURVEY_TOKEN_MAX_AGE


class SurveyCreationEmail(mixins.BuildAbsoluteURIMixin, DisparityEmail):
    template_name = 'salary/mail/survey_created.html'
    subject = 'Salary Survey Created'

    def __init__(self, email, token):
        self.to = email
        self.token = token

    def get_context_data(self, **kwargs):
        kwargs = super(SurveyCreationEmail, self).get_context_data(**kwargs)
        kwargs.update({
            'token': self.token,
            'expires_at': timezone.now() + timezone.timedelta(seconds=SURVEY_TOKEN_MAX_AGE),
            'survey_url': self.build_absolute_uri(
                reverse('survey-detail', kwargs={'token': self.token})
            ),
        })
        return kwargs

send_survey_creation_email = SurveyCreationEmail.as_callable()
