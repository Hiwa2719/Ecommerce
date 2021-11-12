from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from ecommerce.utils import unique_slug_generator
from products.models import Product, Category, Tag, Brand


@receiver(pre_save, sender=Brand)
@receiver(pre_save, sender=Tag)
@receiver(pre_save, sender=Category)
@receiver(pre_save, sender=Product)
def product_abstract_model_pre_save(sender, instance, **kwargs):
    instance.name = instance.name.lower()
    if instance.pk:
        if sender.objects.get(pk=instance.pk).name != instance.name:
            instance.slug = unique_slug_generator(instance)
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
