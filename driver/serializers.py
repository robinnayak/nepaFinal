from rest_framework import serializers
from .models import PushAlertNotification
from authentication.serializers import CustomUserSerializer, OrganizationSerializer, DriverSerializer
from organization.serializers import TripSerializer
from authentication.models import CustomUser, Driver
from organization.models import Trip


class PushAlertNotificationSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    driver = DriverSerializer(read_only=True)
    trip = TripSerializer(read_only=True)
    class Meta:
        model = PushAlertNotification
        fields = '__all__'

    def create(self, validated_data):
        # print(f"self context: {self.context}")
        # print(f"Validated Data: {validated_data}")
        user_email = self.context['user']
        driver = validated_data.pop('driver')
        trip = validated_data.pop('trip')
        title = validated_data.get('title')
        message = validated_data.get('message')
       
        # print("user user email",user_email)
        # print(f"Driver ID: {driver}")
        # print(f"Trip ID: {trip}")
        # print(f"Title: {title}")
        # print(f"Message: {message}")

        try:
            user = CustomUser.objects.get(email=user_email)
            # print(f"User: {user}")
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError({"user": "User not found."})

        try:
            driver = Driver.objects.get(id=driver.id)
            # print(f"Driver: {driver}")
        except Driver.DoesNotExist:
            raise serializers.ValidationError({"driver": "Driver not found."})

        try:
            trip = Trip.objects.get(id=trip.id)
            # print(f"Trip: {trip}")
        except Trip.DoesNotExist:
            raise serializers.ValidationError({"trip": "Trip not found."})

        notification, created = PushAlertNotification.objects.update_or_create(
            user=user,
            driver=driver,
            trip=trip,
            title=title,
            message=message
        )
        print(f"Notification: {notification}, Created: {created}")

        return notification







# class PushAlertNotificationSerializer(serializers.ModelSerializer):
#     user = CustomUserSerializer(read_only=True)

#     class Meta:
#         model = PushAlertNotification
#         fields = ['user','driver','trip','title','message']

#     def create(self, validated_data):
#         user_id = self.context['user']
#         driver_id = self.context['driver']
#         trip_id = self.context['trip']
        
#         print("user_id",user_id)
#         print("driver id",driver_id)
#         print("trip_id", trip_id)

#         try:
#             user = CustomUser.objects.get(id=user_id)
#         except CustomUser.DoesNotExist:
#             raise serializers.ValidationError({"user": "User not found."})

#         try:
#             driver = Driver.objects.get(id=driver_id)
#         except Driver.DoesNotExist:
#             raise serializers.ValidationError({"driver": "Driver not found."})

#         try:
#             trip = Trip.objects.get(id=trip_id)
#         except Trip.DoesNotExist:
#             raise serializers.ValidationError({"trip": "Trip not found."})

#         notification = PushAlertNotification.objects.update_or_create(
#             user=user,
#             driver=driver,
#             trip=trip,
#             **validated_data
#             # title=validated_data.get('title'),
#             # message=validated_data.get('message')
#         )
#         print("notification message", notification)

#         return notification
