from django.shortcuts import render


# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
# models here 
from organization.models import Booking,Trip
from .models import PushAlertNotification
from authentication.models import Driver,Organization,CustomUser
from authentication.serializers import OrganizationSerializer, DriverSerializer
# serializers here 

from .serializers import PushAlertNotificationSerializer
from passenger.models import Passenger
# Create your views here.

class DriverRelatedOrganizationView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        if request.user.is_driver:
            driver = Driver.objects.get(user=request.user)
            organization = driver.organization
            serializer = OrganizationSerializer(organization)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error':'You are not a driver'}, status=status.HTTP_400_BAD_REQUEST)   

class PushAlertNotificationAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
            user = request.user
            try:
                if not user.is_driver and not user.is_organization:
                    # User is a passenger
                    notifications = PushAlertNotification.objects.filter(user__username=user.username)
                    serializer = PushAlertNotificationSerializer(notifications, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)

                elif user.is_driver:
                    # User is a driver
                    driver = Driver.objects.get(user=user)
                    notifications = PushAlertNotification.objects.filter(driver=driver)
                    serializer = PushAlertNotificationSerializer(notifications, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)

                elif user.is_organization:
                    # User is an organization
                    organization = Organization.objects.get(user=user)
                    notifications = PushAlertNotification.objects.filter(trip__organization=organization)
                    serializer = PushAlertNotificationSerializer(notifications, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)

                return Response({"error": "Invalid user type."}, status=status.HTTP_400_BAD_REQUEST)
            
            except Driver.DoesNotExist:
                return Response({"error": "Driver not found."}, status=status.HTTP_404_NOT_FOUND)

            except Organization.DoesNotExist:
                return Response({"error": "Organization not found."}, status=status.HTTP_404_NOT_FOUND)

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    def post(self, request, *args, **kwargs):
        user = request.user
        try:
            if user.is_driver:
                trip_id = request.data.get('trip_id')
                title = request.data.get('title')
                message = request.data.get('message')

                # print(f"User: {user.email}")
                # print(f"Trip ID: {trip_id}")
                # print(f"Title: {title}")
                # print(f"Message: {message}")

                if not trip_id or not title or not message:
                    return Response({"error": "Trip ID, title, and message are required."}, status=status.HTTP_400_BAD_REQUEST)

                driver = Driver.objects.get(user__email=user.email)
                trip = Trip.objects.get(trip_id=trip_id)
                bookings = Booking.objects.filter(tripprice__trip=trip)
                # print(f"Driver: {driver}")
                # print(f"Trip: {trip}")
                # print(f"Bookings: {bookings}")

                notifications = []

                for booking in bookings:
                    passenger_user = CustomUser.objects.get(username=booking.passenger.user.username)
                    print("passenger",passenger_user.email)
                    notification_data = {
                        'user': passenger_user.email,
                        'driver': driver.id,
                        'trip': trip.id,
                        'title': title,
                        'message': message
                    }
                    # print(f"Notification Data: {notification_data}")

                    serializer = PushAlertNotificationSerializer(data=notification_data,context=notification_data)
                    if serializer.is_valid():
                        serializer.save()
                        notifications.append(serializer.data)
                        # print(f"Saved Notification: {serializer.data}")
                    else:
                        print(f"Errors: {serializer.errors}")
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
                return Response(notifications, status=status.HTTP_201_CREATED)
            return Response({"error": "You are not authorized to post notifications."}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            print(f"Exception: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

