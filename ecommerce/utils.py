from django.contrib import messages
from django.utils.translation import ngettext


class AdminMessageMixin:
    def message_mixin(self, request, updated, items, status):
        message = ngettext(
            '{} {} got {} successfully.',
            '{} {}s got {} successfully.',
            updated
        ).format(updated, items, status)
        return self.message_user(request, message, messages.SUCCESS)
