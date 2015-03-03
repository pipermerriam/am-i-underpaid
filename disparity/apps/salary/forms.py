import collections

from django import forms
from django.core.validators import (
    EmailValidator,
)


class SurveyCreateForm(forms.Form):
    owner_email = forms.EmailField(
        label='Your Email Address', help_text=(
            "Your email address will only be used to email you a special link "
            "that allows you to see the survey results and administer the "
            "survey."
        ),
    )
    owner_salary = forms.IntegerField(
        label='Your Salary', help_text=(
            "Your salary information is not directly stored in the database."
        ),
    )
    participant_emails = forms.CharField(
        help_text=(
            "Comma delimited list of email addresses.  Newlines and spaces will "
            "be stripped."
        ),
        widget=forms.Textarea,
    )

    def clean_participant_emails(self):
        unparsed_emails = self.cleaned_data['participant_emails']
        emails = [
            email.strip() for email in unparsed_emails.split(',') if email.strip()
        ]
        validator = EmailValidator()
        for email in emails:
            try:
                validator(email)
            except forms.ValidationError:
                self.add_error(
                    'participant_emails',
                    "{0} is not a valid email address".format(email),
                )
        if len(emails) < 4:
            self.add_error(
                'participant_emails',
                "Too few email addresses",
            )
        duplicates = [
            email for email, count in collections.Counter(emails).items() if count > 1
        ]
        if duplicates:
            self.add_error(
                'participant_emails',
                "The email address(es) {0} appear more than once".format(duplicates),
            )

        owner_email = self.cleaned_data['owner_email']
        if owner_email in emails:
            self.add_error(
                'participant_emails',
                "The survey owner email cannot be in the participant list"
            )

        return emails


class SalaryForm(forms.Form):
    salary = forms.IntegerField()
