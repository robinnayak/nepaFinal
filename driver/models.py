from django.db import models
from authentication.models import CustomUser, Driver
from organization.models import Trip, Booking


class PushAlertNotification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
