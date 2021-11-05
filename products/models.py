from django.db import models
from django.utils.translation import gettext_lazy as _

from ecommerce.utils import unique_slug_generator


class ProductAbstractBaseModel(models.Model):
    """
    this abstract model contains name & slug field
    """
    name = models.CharField(max_length=256)
    slug = models.SlugField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug_generator(self)
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class Product(ProductAbstractBaseModel):
    """
    Product main model
    """
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text='Instead of deleting a product just make it de-active from here')
    is_digital = models.BooleanField(_('digital status'), default=False,
                                     help_text='Designated whether a product is a digital product')
    last_update = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)

    descriptions = models.ManyToManyField('Description', blank=True)
    tags = models.ManyToManyField('Tag', blank=True)


class Description(models.Model):
    title = models.CharField(_('title'), max_length=128, help_text='short description')
    content = models.TextField(_('content'))

    def __str__(self):
        return self.title

    @property
    def summery(self):
        return self.content[:70]


class Tag(ProductAbstractBaseModel):
    pass


class Category(ProductAbstractBaseModel):
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True,
                               help_text='shows the parent category of this one')

    def has_parent(self):
        return self.parent

    class Meta:
        verbose_name_plural = 'Categories'
