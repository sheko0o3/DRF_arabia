from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings

# Create your models here.

# Guest -- Movie -- Reservation


class Movie(models.Model):
    hall = models.CharField(max_length=10)
    movie = models.CharField(max_length=10)

    def __str__(self):
        return self.movie


class Guest(models.Model):
    name = models.CharField(max_length=30)
    mobile = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class Reservation(models.Model):
    guest = models.ForeignKey(to=Guest, on_delete=models.CASCADE, related_name="reservations")
    movie = models.ForeignKey(to=Movie, on_delete=models.CASCADE, related_name="reservations")


class Post(models.Model):
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    body = models.TextField()


# Auto Generated Tokens For Users BY Signals
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)



