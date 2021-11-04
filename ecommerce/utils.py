from datetime import datetime

from django.contrib import messages
from django.utils.translation import ngettext


class AdminMessageMixin:
    """a custom mixin for showing messages of custom actions inside admin panel"""

    def message_mixin(self, request, updated, items, status):
        message = ngettext(
            '{} {} got {} successfully.',
            '{} {}s got {} successfully.',
            updated
        ).format(updated, items, status)
        return self.message_user(request, message, messages.SUCCESS)


def get_past_dates(now=None, years=0, months=0, days=0):
    """
    we gave this function a timestamp from now in past based on number of days or months or years and it gives
    us the date.
    some dates my not be in calendar so it chooses the closest older date
    """
    if not now:
        now = datetime.now()
    year = now.year - years
    month = now.month - months
    day = now.day - days
    if day < 1:
        month -= 1
        day += 31
    if month < 1:
        year -= 1
        month += 12
    try:
        return datetime(year=year, month=month, day=day, hour=0, minute=0, second=0)
    except ValueError:
        now = datetime(year=year, month=month, day=1)
        return get_past_dates(now, days=-(day - 2))
