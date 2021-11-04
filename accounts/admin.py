from datetime import datetime

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from ecommerce.mixins import AdminMessageMixin
from ecommerce.utils import get_past_dates, activate, deactivate

User = get_user_model()


class LastLoginTimeSince(admin.SimpleListFilter):
    """
    this filter aims to categorize users according to the time from their last login

    1.last week --> now
    2.last month --> last week
    3.six months --> last month
    4.last year --> six month
    5.more than a year
    """

    title = _('timesince form last login')
    parameter_name = 'time'

    def __init__(self, request, params, model, model_admin):
        now, last_week, last_month, last_six_months, last_year = self.get_dates()
        queryset = model_admin.get_queryset(request)
        self.week_query = queryset.filter(last_login__range=(last_week, now))
        self.month_query = queryset.filter(last_login__range=(last_month, last_week))
        self.six_month_query = queryset.filter(last_login__range=(last_six_months, last_month))
        self.year_query = queryset.filter(last_login__range=(last_year, last_six_months))
        self.year_plus_query = queryset.filter(last_login__lt=last_year)
        super().__init__(request, params, model, model_admin)

    def lookups(self, request, model_admin):
        """
        lookups that will appear on the right hand side of the admin panel
        """
        if self.week_query.exists():
            yield '1W', _('past 7 days')
        if self.month_query.exists():
            yield '1M', _('last month to last week')
        if self.six_month_query.exists():
            yield '6M', _('six month ago to last month')
        if self.year_query.exists():
            yield '1Y', _('last year to six month ago')
        if self.year_plus_query.exists():
            yield '1Y+', _('more than a year')

    def queryset(self, request, queryset):
        """
        according to chosen filter returns data queryset
        """
        if self.value() == '1W':
            return self.week_query
        if self.value() == '1M':
            return self.month_query
        if self.value() == '6M':
            return self.six_month_query
        if self.value() == '1Y':
            return self.year_query
        if self.value() == '1Y+':
            return self.year_plus_query

    @staticmethod
    def get_dates():
        """
        gets different date-times
        """
        now = datetime.now()
        last_week = get_past_dates(now, days=7)
        last_month = get_past_dates(now, months=1)
        last_six_months = get_past_dates(now, months=6)
        last_year = get_past_dates(now, years=1)
        return now, last_week, last_month, last_six_months, last_year


@admin.register(User)
class UserAdmin(BaseUserAdmin, AdminMessageMixin):
    actions = [activate, deactivate]
    list_display = 'email', 'username', 'is_active', 'is_staff'
    list_filter = 'is_active', 'is_staff', 'is_superuser', LastLoginTimeSince, 'date_joined', 'groups'
    ordering = None
    search_fields = 'email', 'username'

    readonly_fields = 'date_joined',
    filter_horizontal = 'user_permissions', 'groups'

    fieldsets = [
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('username',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions', 'groups')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')})
    ]
    add_fieldsets = [
        (None, {
            'fields': ('email', 'password1', 'password2')
        })
    ]

# @admin.register(Permission)
# class PermissionModelAdmin(admin.ModelAdmin):
#     search_fields = 'name',
