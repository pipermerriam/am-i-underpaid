import random

from django.db import models
from django.utils import timezone

import uuidfield


def get_default_total():
    return random.randint(1e9, 1e12)


class Survey(models.Model):
    uuid = uuidfield.UUIDField(auto=True, version=4, hyphenate=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    # This field stores the running total of all of the collected salaries
    # while salaries are being collected, and the average salary if collection
    # has completed.
    total = models.BigIntegerField(default=get_default_total)
    # The tracker field stores a VERY large number that is used to enforce one
    # response per participant.  Each link sent to a participant has a large
    # prime number embedded in it.  Each time a response is entered, the
    # `tracker` number is multiplied by that number.  This way, we can know if
    # someone has already responded by checking to see if the tracker number is
    # divisible by the prime that was assigned to them.
    _tracker = models.CharField(default='1', max_length=10000, null=True)

    num_collected = models.PositiveIntegerField(default=0, null=True)
    num_expected = models.PositiveIntegerField(null=True)

    @property
    def tracker(self):
        if self._tracker is None:
            return None
        return long(self._tracker)

    @tracker.setter
    def tracker(self, value):
        if value is None:
            self._tracker = None
        else:
            self._tracker = str(value)

    def has_key_been_recorded(self, key):
        if self.tracker is None:
            return None
        return self.tracker % key == 0

    def record_salary(self, salary, key):
        if self.has_key_been_recorded(key):
            raise ValueError("This key has already recorded a salary")
        self.tracker *= key
        self.total += salary
        self.num_collected += 1
        self.save()

    @property
    def is_open(self):
        return self.tracker is not None

    @property
    def is_finalized(self):
        return not self.is_open

    @property
    def is_finalizable(self):
        return self.num_collected >= 4

    def finalize(self, seed):
        if not self.is_finalizable:
            raise ValueError("Survey must have at least 4 responses to be finalized")
        total = self.total - seed
        self.total = total / self.num_collected
        self.num_collected = None
        self.num_expected = None
        self.tracker = None
        self.save()
