import pytest

from disparity.apps.salary.utils import (
    get_survey_unique_primes,
    PRIMES,
)


def test_util_function_to_pair_primes_with_emails(factories):
    emails = factories.EmailAddressFactory.create_batch(10)
    pairs = get_survey_unique_primes(*emails)
    primes = [p for e, p in pairs]

    assert len(pairs) == len(emails)
    assert len(set(primes)) == len(emails)
    assert not set(primes).difference(PRIMES)


def test_too_many_emails(factories):
    emails = factories.EmailAddressFactory.create_batch(len(PRIMES) + 1)

    with pytest.raises(ValueError):
        get_survey_unique_primes(*emails)
