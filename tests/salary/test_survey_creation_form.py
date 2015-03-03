from disparity.apps.salary.forms import (
    SurveyCreateForm,
)


def test_with_invalid_email_addresses():
    data = {
        'owner_email': 'owner@example.com',
        'owner_salary': 12345,
        'participant_emails': (
            'test-1@example.com,'
            'invalid-1,'
            'test-2@example.com,'
            'invalid-2,'
            'test-3@example.com,'
            'test-4@example.com,'
        ),
    }
    form = SurveyCreateForm(data=data)
    assert not form.is_valid()
    assert 'participant_emails' in form.errors
    assert any(
        ['invalid-1' in err for err in form.errors['participant_emails']]
    ), form.errors['participant_emails']
    assert any(
        ['invalid-2' in err for err in form.errors['participant_emails']]
    ), form.errors['participant_emails']


def test_with_too_few_participants():
    data = {
        'owner_email': 'owner@example.com',
        'owner_salary': 12345,
        'participant_emails': (
            'test-1@example.com,'
            'test-2@example.com,'
            'test-3@example.com,'
        ),
    }
    form = SurveyCreateForm(data=data)
    assert not form.is_valid()
    assert 'participant_emails' in form.errors
    assert any(
        ['Too few' in err for err in form.errors['participant_emails']]
    ), form.errors['participant_emails']


def test_valid_participant_emails_are_parsed():
    data = {
        'owner_email': 'owner@example.com',
        'owner_salary': 12345,
        'participant_emails': (
            'test-1@example.com,'
            'test-2@example.com,'
            'test-3@example.com,'
            'test-4@example.com,'
        ),
    }
    form = SurveyCreateForm(data=data)
    assert form.is_valid(), form.errors

    expected = set((
        'test-1@example.com',
        'test-2@example.com',
        'test-3@example.com',
        'test-4@example.com',
    ))
    assert not expected.symmetric_difference(form.cleaned_data['participant_emails'])


def test_duplicate_participant_email_is_error():
    data = {
        'owner_email': 'owner@example.com',
        'owner_salary': 12345,
        'participant_emails': (
            'test-1@example.com,'
            'test-1@example.com,'  # Duplicate
            'test-2@example.com,'
            'test-3@example.com,'
            'test-4@example.com,'
        ),
    }
    form = SurveyCreateForm(data=data)
    assert not form.is_valid()
    assert 'participant_emails' in form.errors
    assert any(
        ['test-1@example.com' in err for err in form.errors['participant_emails']]
    )


def test_owner_email_in_participants_is_error():
    data = {
        'owner_email': 'owner@example.com',
        'participant_emails': (
            'test-1@example.com,'
            'owner@example.com,'
            'test-2@example.com,'
            'test-3@example.com,'
            'test-4@example.com,'
        ),
    }
    form = SurveyCreateForm(data=data)
    assert not form.is_valid()
    assert 'participant_emails' in form.errors
    assert any(
        ['owner' in err for err in form.errors['participant_emails']]
    )
