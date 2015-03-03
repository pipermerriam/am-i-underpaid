import random
from dateutil import parser

from django.utils import timezone
from django.core import signing

from .primes import PRIMES


SURVEY_TOKEN_SALT = 'salary:survey'
SURVEY_TOKEN_MAX_AGE = 60 * 60 * 24 * 7  # 7 days


def get_survey_unique_primes(*emails):
    if len(emails) > len(PRIMES):
        raise ValueError("Not enough primes")
    return zip(
        emails,
        random.sample(PRIMES, len(emails)),
    )


def generate_survey_token(seed, prime_identifier, is_admin, survey_id):
    return signing.dumps({
        'seed': seed,
        'prime_identifier': prime_identifier,
        'is_admin': is_admin,
        'survey_id': str(survey_id),
        'expires_at': str(timezone.now() + timezone.timedelta(seconds=SURVEY_TOKEN_MAX_AGE)),
    }, salt=SURVEY_TOKEN_SALT)


def unsign_survey_token(token):
    data = signing.loads(
        token, salt=SURVEY_TOKEN_SALT, max_age=SURVEY_TOKEN_MAX_AGE,
    )
    expires_at_str = data.pop('expires_at')
    data['expires_at'] = parser.parse(expires_at_str)
    return data
