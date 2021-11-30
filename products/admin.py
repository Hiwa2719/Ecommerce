import re

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from ecommerce.mixins import AddFieldSetsMixin, AdminMessageMixin
from ecommerce.utils import activate, deactivate
from .forms import CategoryForm, ProductForm
from .models import Product, Description, Tag, Category, Image, Brand


@admin.register(Product)
class ProductModelAdmin(AddFieldSetsMixin, admin.ModelAdmin):
    actions = activate, deactivate
    search_fields = 'name', 'slug', 'descriptions__title', 'descriptions__content'
    list_display = '__str__', 'is_active', 'is_digital'
    list_filter = 'is_active', 'is_digital', 'last_update', 'created_date'
    filter_horizontal = 'descriptions', 'tags', 'categories', 'images',
    readonly_fields = 'slug',
    fieldsets = [
        (_('Product Info'), {
            'fields': ('name', 'slug', 'is_active', 'is_digital')
        }),
        (_('Relations'), {
            'fields': ('brand', 'categories', 'descriptions', 'features', 'images', 'tags', 'features_excel')
        })
    ]
    add_fieldsets = [
        (None, {
            'fields': ('name', 'is_active', 'is_digital', 'descriptions', 'features_excel')
        })
    ]
    form = ProductForm


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


@admin.register(Image)
class ImageModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Brand)
class BrandModelAdmin(AddFieldSetsMixin, admin.ModelAdmin):
    list_display = '__str__', 'slug'
    search_fields = 'name', 'slug', 'descriptions__title', 'descriptions__content', 'categories__name'
    filter_horizontal = 'categories', 'descriptions', 'images'
    readonly_fields = 'slug',

    add_fieldsets = [
        (None, {
            'fields': ('name', 'categories', 'descriptions', 'images')
        })
    ]

    fieldsets = [
        (_('Brand Info'), {
            'fields': ('name', 'slug')
        }),
        (_('Relations'), {
            'fields': ('categories', 'descriptions', 'images')
        })
    ]


# @admin.register(Feature)
# class FeatureModelAdmin(admin.ModelAdmin):
#     list_display = '__str__',
#     list_filter = 'parent_feature',
#     search_fields = 'parent_feature', 'value'
#
#     form = FeatureForm
