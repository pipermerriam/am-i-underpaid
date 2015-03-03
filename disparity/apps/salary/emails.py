from emailtools import mixins

from django.core.urlresolvers import reverse

from disparity.apps.core.emails import DisparityEmail
from disparity.apps.salary.utils import (
    unsign_survey_token,
)


class SurveyCreationEmail(mixins.BuildAbsoluteURIMixin, DisparityEmail):
    template_name = 'salary/mail/survey_created.html'
    subject = 'Salary Survey Created'

    def __init__(self, email, token):
        self.to = email
        self.token = token

    def get_context_data(self, **kwargs):
        context = super(SurveyCreationEmail, self).get_context_data(**kwargs)
        context.update({
            'token': self.token,
            'survey_url': self.build_absolute_uri(
                reverse('survey-detail', kwargs={'token': self.token})
            ),
        })
        context.update(unsign_survey_token(self.token))
        return context

send_survey_creation_email = SurveyCreationEmail.as_callable()
