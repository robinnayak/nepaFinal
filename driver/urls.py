from django.urls import path
from . import views
from authentication.views import  DriverDetailView
urlpatterns = [
    path('driver-related-organization/',views.DriverRelatedOrganizationView.as_view(),name="driver_related_organization"),
    path('push-alert/',views.PushAlertNotificationAPIView.as_view(),name='push_alert'),

]


