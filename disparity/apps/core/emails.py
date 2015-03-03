from django.conf import settings

from emailtools import MarkdownEmail


class DisparityEmail(MarkdownEmail):
    from_email = settings.DEFAULT_FROM_EMAIL

    def get_subject(self):
        return "[Are We Being Underpaid] {0}".format(self.subject)
