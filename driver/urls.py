from django.urls import path
from . import views

urlpatterns = [
    path('driver-related-organization/',views.DriverRelatedOrganizationView.as_view(),name="driver_related_organization")
]
