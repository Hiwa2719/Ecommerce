from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CommentModelAdmin(admin.ModelAdmin):
    list_display = 'user', 'product', 'positivity', 'publish_date'
    list_filter = 'publish_date',
    search_fields = 'product__name', 'content'

    @admin.display(description='recommend')
    def positivity(self, obj):
        if obj.rating == 'pos':
            return 'Yes'
        return 'No'
