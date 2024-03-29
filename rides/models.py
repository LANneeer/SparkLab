from django.db import models
from users.models import User


class Ride(models.Model):
    user = models.ManyToManyField(User, related_name='rides', blank=True, through='RideRequest')
    ride_title = models.CharField(max_length=255)
    ride_description = models.TextField()
    max_passengers = models.PositiveIntegerField(default=4)
    departure = models.DateTimeField()
    arrival = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.ride_title} - {self.departure}'

    class Meta:
        verbose_name = 'Поездка'
        verbose_name_plural = 'Поездки'
        ordering = ('-created_at',)


class RideRequest(models.Model):
    statuses = (
        ('pending', 'В ожидании'),
        ('approved', 'Одобрено'),
        ('rejected', 'Отклонено'),
        ('canceled', 'Отменено')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ride_requests')
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE, related_name='ride_requests')
    status = models.CharField(max_length=50, choices=statuses, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.ride.ride_title}'

    class Meta:
        verbose_name = 'Заявка на поездку'
        verbose_name_plural = 'Заявки на поездку'
        ordering = ('-created_at',)
