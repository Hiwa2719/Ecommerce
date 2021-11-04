from django.db import models


class ProductAbstractBaseModel(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = unique_slug_generator(self.name)
        super().save(*args, **kwargs)
