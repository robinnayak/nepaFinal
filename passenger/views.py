from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Passenger   
from .serializers import PassengerSerializer
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class PassengerView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        if not request.user.is_driver and not request.user.is_organization:
            passengers = Passenger.objects.get(user=request.user)
            serializer = PassengerSerializer(passengers)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'error':'You are not a passenger'}, status=status.HTTP_400_BAD_REQUEST)
            
        
