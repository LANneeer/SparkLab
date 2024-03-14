from django.db import models
from users.models import User


class Ride(models.Model):
    user = models.ManyToManyField(User, related_name='rides', blank=True)
    ride_title = models.CharField(max_length=255)
    ride_description = models.TextField()
    departure = models.DateTimeField()
    arrival = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.ride_title} - {self.departure}'

    class Meta:
        verbose_name = 'Поездка'
        verbose_name_plural = 'Поездки'
        ordering = ('-created_at',)
