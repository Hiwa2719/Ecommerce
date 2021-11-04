import random
import string
from datetime import datetime

from django.contrib import messages
from django.utils.text import slugify
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


def unique_string_generator(number_of_chars=7, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(number_of_chars))


def unique_slug_generator(instance, new_slug=None, number_of_chars=4):
    if new_slug:
        slug = new_slug
    else:
        slug = slugify(instance.name)

    if instance.__class__.objects.filter(slug=slug).exists():
        new_slug = f'{slug}-{unique_string_generator()}'
        return unique_slug_generator(instance, new_slug=new_slug, number_of_chars=number_of_chars)
    return slug
