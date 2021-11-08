import re

from django.contrib import admin

from ecommerce.mixins import AddFieldSetsMixin, AdminMessageMixin
from ecommerce.utils import activate, deactivate
from .forms import CategoryForm
from .models import Product, Description, Tag, Category


@admin.register(Product)
class ProductModelAdmin(AddFieldSetsMixin, admin.ModelAdmin):
    actions = activate, deactivate
    search_fields = 'name', 'slug', 'descriptions__title', 'descriptions__content'
    list_display = '__str__', 'is_active', 'is_digital'
    list_filter = 'is_active', 'is_digital', 'last_update', 'created_date'
    filter_horizontal = 'descriptions',
    readonly_fields = 'slug',
    add_fieldsets = [
        (None, {
            'fields': ('name', 'is_active', 'is_digital', 'descriptions')
        })
    ]


@admin.register(Description)
class DescriptionModelAdmin(admin.ModelAdmin):
    list_display = 'title', 'summery'
    search_fields = 'title', 'content'


@admin.register(Tag)
class TagModelAdmin(AddFieldSetsMixin, admin.ModelAdmin):
    list_display = 'name', 'slug'
    search_fields = 'name', 'slug'
    readonly_fields = 'slug',

    add_fieldsets = [
        (None, {
            'fields': ('name',)
        })
    ]


@admin.action(permissions=['change'], description='clear parent of select items')
def clear_parent(model_admin, request, queryset):
    updated = queryset.update(parent=None)
    model_admin.message_mixin(request, updated, 'category', 'unparent')


@admin.register(Category)
class CategoryModelAdmin(AdminMessageMixin, AddFieldSetsMixin, admin.ModelAdmin):
    actions = clear_parent,
    list_display = 'name', 'slug', 'parent'
    readonly_fields = 'slug',
    search_fields = 'name', 'slug',

    autocomplete_fields = 'parent',
    add_fieldsets = [
        (None, {
            'fields': ('name', 'parent')
        })
    ]
    form = CategoryForm

    def get_search_results(self, request, queryset, search_term):
        result = super().get_search_results(request, queryset, search_term)
        match = re.search('category/[0-9]+/change/', request.META.get('HTTP_REFERER'))
        if match and request.path_info == '/admin/autocomplete/':
            pk_match = re.search(r'[0-9]+', match.group())
            if pk_match:
                queryset = result[0].exclude(pk=int(pk_match.group()))
                return queryset, result[1]
        return result
