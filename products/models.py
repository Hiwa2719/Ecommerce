from django.db import models
from django.db.models.constraints import UniqueConstraint
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class ProductAbstractBaseModel(models.Model):
    """
    this abstract model contains name & slug field
    """
    name = models.CharField(max_length=256)
    slug = models.SlugField()

    def __str__(self):
        return self.name.capitalize()

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
    categories = models.ManyToManyField('Category', blank=True)
    images = models.ManyToManyField('Image', blank=True)
    # features = models.ManyToManyField('Feature', blank=True)
    features = models.JSONField()
    brand = models.ForeignKey('Brand', on_delete=models.SET_NULL, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('products:product_detail', kwargs={'slug': self.slug})


class Description(models.Model):
    title = models.CharField(_('title'), max_length=128, help_text='short description')
    content = models.TextField(_('content'))

    def __str__(self):
        return self.title

    @property
    def summery(self):
        return self.content[:70]


class Tag(ProductAbstractBaseModel):
    class Meta:
        constraints = UniqueConstraint(fields=('name',), name='unique name'),


class Category(ProductAbstractBaseModel):
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True,
                               help_text='shows the parent category of this one')

    class Meta:
        verbose_name_plural = 'Categories'


class Brand(ProductAbstractBaseModel):
    descriptions = models.ManyToManyField('Description', blank=True)
    images = models.ManyToManyField('Image', blank=True)
    categories = models.ManyToManyField('Category', blank=True)


def image_upload_location():
    pass


class Image(models.Model):
    name = models.CharField(max_length=128, blank=True)
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return self.image.name


# class Feature(models.Model):
#     # name = models.CharField(_('name'), max_length=128)
#     value = models.TextField(_('Value'))
#     parent_feature = models.ForeignKey('self', on_delete=models.CASCADE,
#                                        help_text='for products with multiple sub features', blank=True, null=True)
#
#     def __str__(self):
#         if self.parent_feature:
#             return str(self.parent_feature) + '-->' + self.value
#         return self.value
#
#     class Meta:
#         constraints = [UniqueConstraint(fields=['parent_feature', 'value'], name='parent-value uniqueness')]
