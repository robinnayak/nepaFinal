from django.urls import path
from . import views
from authentication.views import  DriverDetailView
urlpatterns = [
<<<<<<< HEAD
    path('',DriverDetailView.as_view(), name='drivers'),
=======
    path('driver-related-organization/',views.DriverRelatedOrganizationView.as_view(),name="driver_related_organization"),
    path('push-alert/',views.PushAlertNotificationAPIView.as_view(),name='push_alert'),
>>>>>>> aa02306 (push notificaton updated)
]


