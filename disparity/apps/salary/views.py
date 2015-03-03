from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.core import signing
from django.http import Http404
from django.views.generic import (
    FormView,
    View,
)

from disparity.apps.salary.utils import (
    get_survey_unique_primes,
    generate_survey_token,
    unsign_survey_token,
)
from disparity.apps.salary.emails import (
    send_survey_creation_email,
)
from disparity.apps.salary.forms import (
    SurveyCreateForm,
    SalaryForm,
)
from disparity.apps.salary.models import (
    Survey,
)


class SurveyCreateView(FormView):
    template_name = 'salary/survey_create.html'
    model = Survey
    form_class = SurveyCreateForm

    def form_valid(self, form):
        owner_email = form.cleaned_data['owner_email']
        participant_emails = form.cleaned_data['participant_emails']
        all_emails = [owner_email] + participant_emails
        survey = Survey.objects.create(
            num_expected=len(participant_emails) + 1,
        )
        seed = survey.total
        prime_lookups = dict(get_survey_unique_primes(owner_email, *participant_emails))
        survey.record_salary(
            form.cleaned_data['owner_salary'],
            key=prime_lookups[owner_email],
        )
        owner_token = generate_survey_token(
            seed=seed,
            email=owner_email,
            all_emails=all_emails,
            survey_id=survey.uuid,
            prime_identifier=prime_lookups[owner_email],
            is_admin=True,
        )
        # Send the owner their email/token
        send_survey_creation_email(email=owner_email, token=owner_token)
        for email in participant_emails:
            participant_token = generate_survey_token(
                seed=seed,
                email=email,
                all_emails=all_emails,
                survey_id=survey.uuid,
                prime_identifier=prime_lookups[email],
                is_admin=False,
            )
            send_survey_creation_email(email=email, token=participant_token)
        return redirect(reverse('survey-detail', kwargs={'token': owner_token}))


class WithTokenVerificationMixin(object):
    def get_object(self):
        self.token = self.kwargs['token']
        try:
            self.token_data = unsign_survey_token(self.token)
        except signing.BadSignature:
            raise Http404

        survey_uuid = self.token_data['survey_id']
        self.object = Survey.objects.get(uuid=survey_uuid)
        return self.object


class SurveyDetailView(WithTokenVerificationMixin, FormView):
    template_name = 'salary/survey_detail.html'
    form_class = SalaryForm

    def get_context_data(self, **kwargs):
        context = super(SurveyDetailView, self).get_context_data(**kwargs)
        context['survey'] = self.get_object()
        context['token'] = self.token
        context['key_has_been_submitted'] = self.object.has_key_been_recorded(
            self.token_data['prime_identifier']
        )
        context.update(self.token_data)
        return context

    def form_valid(self, form):
        survey = self.get_object()
        if survey.has_key_been_recorded(self.token_data['prime_identifier']):
            form.add_error(None, "You have already submitted your salary")
            return self.form_invalid(form)

        if survey.is_finalized:
            form.add_error(None, "This survey has already been finalized")
            return self.form_invalid(form)

        if survey.is_open:
            survey.record_salary(
                form.cleaned_data['salary'], key=self.token_data['prime_identifier'],
            )
            if survey.num_collected >= survey.num_expected:
                survey.finalize(self.token_data['seed'])
            return redirect(reverse('survey-detail', kwargs={'token': self.token}))
        assert False, "Should not be possible"


class SurveyFinalizeView(WithTokenVerificationMixin, View):
    def post(self, *args, **kwargs):
        survey = self.get_object()
        if not survey.is_finalizable:
            raise Http404
        if not self.token_data['is_admin']:
            raise Http404
        survey.finalize(self.token_data['seed'])
        return redirect(reverse('survey-detail', kwargs={'token': self.token}))
