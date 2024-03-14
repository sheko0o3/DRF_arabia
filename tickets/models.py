from django.db import models

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


