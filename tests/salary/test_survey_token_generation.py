import pytest

from disparity.apps.salary.utils import (
    generate_survey_token,
    unsign_survey_token,
)


def test_token_round_trip():
    data_in = {
        'seed': 12345,
        'email': 'test@example.com',
        'is_admin': True,
        'prime_identifier': 5,
        'survey_id': 'some-id',
    }
    token = generate_survey_token(**data_in)
    data_out = unsign_survey_token(token)
    data_out.pop('expires_at')

    assert data_in == data_out
