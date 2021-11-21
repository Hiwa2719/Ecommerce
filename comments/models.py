from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
User = get_user_model()


class Comment(models.Model):
    RATING_CHOICES = [
        ('pos', _('I recommend buying this product.')),
        ('neg', _('I don\'t recommend buying this product.')),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.CharField(max_length=3, choices=RATING_CHOICES)
    content = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    publish_date = models.DateTimeField(blank=True, null=True)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)

    def __str__(self):
        return self.content[:50]
