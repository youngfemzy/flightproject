from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Customer


# THIS SIGNALS.PY IS GOING TO SET SET ALL USERS AS A CUSTOMER, AND WHEN A NEW ACCOUNT IS CREATED
@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(customer=instance)
