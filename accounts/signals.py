from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()


@receiver(post_save, sender=User)
def user_post_save_receiver(sender, instance, created, **kwargs):
    if created:
        send_mail(
            subject='Email verification at ecommerce',
            message='hello dear, you have attempted registering on our website. '
            'for that matter please click on following link.',
            from_email='hiahmadyan@gmail.com',
            recipient_list=[instance.email, ]
        )
