import string
import random
from rest_framework import serializers, status
from rest_framework.response import Response
from .models import Vehicle, Organization, Driver, Trip, Booking, TripPrice, Ticket
from authentication.serializers import OrganizationSerializer, DriverSerializer
from passenger.serializers import PassengerSerializer
from rest_framework.exceptions import ValidationError
from passenger.models import Passenger
class VehicleSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer(read_only=True)
    driver = DriverSerializer(read_only=True)

    class Meta:
        model = Vehicle
        fields = '__all__'

    def create(self, validated_data):
        org_email = self.context.get('org_email')
        dri_license = self.context.get('dri_license')
        check_driver = self.context.get('check_driver')

        validated_data = self._assign_organization_and_driver(validated_data, org_email, dri_license, check_driver)
        if isinstance(validated_data, Response):  # Error response from _assign_organization_and_driver
            return validated_data

        veh_id = self._generate_random_string()
        reg_id = self._generate_registration_number(veh_id, validated_data['organization'].user.username)
        validated_data['registration_number'] = reg_id

        vehicle = Vehicle.objects.create(**validated_data)
        return vehicle

    def update(self, instance, validated_data):
        validated_data.pop('registration_number',None)
        validated_data.pop('license_plate_number',None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance

    def _assign_organization_and_driver(self, validated_data, org_email, dri_license, check_driver):
        try:
            if check_driver and dri_license:
                driver_license = Driver.objects.get(license_number=dri_license)
                validated_data['driver'] = driver_license
            elif not dri_license:
                validated_data['driver'] = None  # Handle cases where there is no driver assigned

            if org_email:
                org_mail = Organization.objects.get(user__email=org_email)
                validated_data['organization'] = org_mail
            else:
                raise ValidationError({"message": "Organization not found"})

        except Organization.DoesNotExist:
            return Response({"message": "Organization not found"}, status=status.HTTP_404_NOT_FOUND)
        except Driver.DoesNotExist:
            return Response({"message": "Driver not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return validated_data

    @staticmethod
    def _generate_random_string(length=10):
        characters = string.ascii_letters + string.digits
        result = ''.join(random.choice(characters) for _ in range(length))
        return result

    @staticmethod
    def _generate_registration_number(id, username):
        prefix = f"{id}{username}"
        return prefix.upper()

class TripSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer(read_only=True)
    class Meta:
        model = Trip
        fields = '__all__'
        
    def create(self, validated_data):
        org_email = self.context.get('org_email')
        print("org_email",org_email)
        try:
            org_mail = Organization.objects.get(user__email=org_email)
            validated_data['organization'] = org_mail
        except Organization.DoesNotExist:
            return Response({"message": "Organization not found"}, status=status.HTTP_404_NOT_FOUND)
        trip = Trip.objects.create(**validated_data)
        return trip
    
    
class TripPriceSerializer(serializers.ModelSerializer):
    trip = TripSerializer(read_only=True)
    vehicle = VehicleSerializer(read_only=True)
    class Meta:
        model = TripPrice
        fields = '__all__'
        
    def create(self,validated_data):
        trip_id = self.context.get('trip_id')
        vehicle_registration_number = self.context.get('vehicle_registration_number')
        org_email = self.context.get('org_email')   
        try:
            if trip_id:
                trip = Trip.objects.get(trip_id=trip_id, organization__user__email=org_email)
                validated_data['trip'] = trip 
            else:
                raise ValidationError({"message": "Trip not found"})
            if vehicle_registration_number:
                vehicle = Vehicle.objects.get(registration_number=vehicle_registration_number, organization__user__email=org_email)
                validated_data['vehicle'] = vehicle
            else:
                raise ValidationError({"message": "Vehicle not found"})
            trip_price = TripPrice.objects.create(**validated_data)
            return trip_price
        except Trip.DoesNotExist:
            return Response({"message": "Trip not found"}, status=status.HTTP_404_NOT_FOUND)
        except Vehicle.DoesNotExist:
            return Response({"message": "Vehicle not found"}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def update(self, instance, validated_data):
        validated_data.pop('trip',None)
        validated_data.pop('vehicle',None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            
        instance.save()
        return instance
class BookingSerializer(serializers.ModelSerializer):
    passenger = PassengerSerializer(read_only=True)
    tripprice = TripPriceSerializer(read_only=True)
    class Meta:
        model = Booking
        fields = '__all__'
        
    def create(self, validated_data):   
        validated_data.pop('tripprice',None)
        validated_data.pop('passenger',None)
        passenger_email = self.context.get('passenger_email')
        trip_price_id = self.context.get('trip_price_id')
        try:
            passenger = Passenger.objects.get(user__email=passenger_email)
            validated_data['passenger'] = passenger
        except Passenger.DoesNotExist:
            return Response({"message": "Passenger not found"}, status=status.HTTP_404_NOT_FOUND)
        try:
            trip_price = TripPrice.objects.get(trip_price_id=trip_price_id)
            validated_data['tripprice'] = trip_price
            
        except TripPrice.DoesNotExist:
            return Response({"message": "Trip Price not found"}, status=status.HTTP_404_NOT_FOUND)
        booking = Booking.objects.create(**validated_data)
        return booking
    
class TicketSerializer(serializers.ModelSerializer):
    booking = BookingSerializer(read_only=True)
    class Meta:
        model = Ticket
        fields = '__all__'
        
    

    
    
    