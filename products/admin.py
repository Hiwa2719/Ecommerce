from django.contrib import admin

from ecommerce.mixins import AddFieldSetsMixin
from ecommerce.utils import activate, deactivate
from .models import Product, Description, Tag


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
