from django.contrib import messages
from django.utils.translation import ngettext


class AddFieldSetsMixin:
    """
    uses add_fieldsets attribute while creating new instances in admin panel
    """
    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)


class AdminMessageMixin:
    """a custom mixin for showing messages of custom actions inside admin panel"""

    def message_mixin(self, request, updated, items, status):
        message = ngettext(
            '{} {} got {} successfully.',
            '{} {}s got {} successfully.',
            updated
        ).format(updated, items, status)
        return self.message_user(request, message, messages.SUCCESS)