from django.db.models.signals import post_save
from django.dispatch import receiver
from billing.models import Price


@receiver(post_save, sender=Price)
def update_active(sender, instance, *args, **kwargs):
    if instance.is_active:
        Price.objects.filter(product__id=instance.product.id,
                             currency=instance.currency,
                             is_active=True
                             ).exclude(id=instance.id).update(is_active=False)
