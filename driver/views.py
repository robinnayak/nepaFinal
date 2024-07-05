from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from authentication.models import Driver,Organization
from authentication.serializers import OrganizationSerializer, DriverSerializer
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
    
        
