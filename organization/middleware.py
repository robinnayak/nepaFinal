from django.utils import timezone
from datetime import timedelta
from .models import Trip

class UpdateTripDatesMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        self.update_trip_dates()
        return response

    def update_trip_dates(self):
        trips = Trip.objects.all()
        for trip in trips:
            trip.start_datetime += timedelta(hours=24)
            trip.end_datetime = timezone.now() + timedelta(hours=6)  # Example duration
            trip.save()