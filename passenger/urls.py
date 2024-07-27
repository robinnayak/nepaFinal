from django.urls import path
from passenger.views import PassengerView,PassengerChatbotView


urlpatterns = [
    path('',PassengerView.as_view(), name='passenger'),
    path('passenger-chatbot/',PassengerChatbotView.as_view(), name='passenger_chatbot'),

]
