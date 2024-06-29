from django.urls import path
from passenger.views import PassengerView


urlpatterns = [
    path('',PassengerView.as_view(), name='passenger'),
]
