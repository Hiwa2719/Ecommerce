from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from ecommerce.utils import AdminMessageMixin

User = get_user_model()


@admin.action(permissions=['change', ], description='make selected items active')
def activate(model_admin, request, queryset):
    updated = queryset.update(is_active=True)
    model_admin.message_mixin(request, updated, 'user', 'active')


@admin.action(permissions=['change', ], description='make selected items de-active')
def deactivate(model_admin, request, queryset):
    updated = queryset.update(is_active=False)
    model_admin.message_mixin(request, updated, 'user', 'de-active')


@admin.register(User)
class UserAdmin(BaseUserAdmin, AdminMessageMixin):
    actions = [activate, deactivate]
