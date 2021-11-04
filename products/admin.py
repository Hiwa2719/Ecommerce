from django.contrib import admin

from ecommerce.utils import activate, deactivate
from .models import Product, Description


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    actions = activate, deactivate
    search_fields = 'name', 'slug', 'descriptions__title', 'descriptions__content'
    list_display = '__str__', 'is_active', 'is_digital'
    list_filter = 'is_active', 'is_digital', 'last_update', 'created_date'
    filter_horizontal = 'descriptions',
    readonly_fields = 'slug',
    add_fieldset = [
        (None, {
            'fields': ('name', 'is_active', 'is_digital', 'descriptions')
        })
    ]

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldset
        return super().get_fieldsets(request, obj)


@admin.register(Description)
class DescriptionModelAdmin(admin.ModelAdmin):
    list_display = 'title', 'summery'
    search_fields = 'title', 'content'
