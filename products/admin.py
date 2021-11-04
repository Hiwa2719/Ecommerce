from django.contrib import admin

from .models import Product


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = '__str__', 'is_active', 'is_digital'
    list_filter = 'is_active', 'is_digital', 'last_update', 'created_date'

    add_fieldset = [
        (None, {
            'fields': ('name', 'is_active', 'is_digital')
        })
    ]

    def get_fieldsets(self, request, obj=None):
        if obj:
            return self.add_fieldset
        return super().get_fieldsets(request, obj)
