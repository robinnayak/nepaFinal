from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Passenger   
from .serializers import PassengerSerializer
from rest_framework.permissions import IsAuthenticated 
# Create your views here.
from passenger.AI.ai_db_chatbot import DatabaseChatbot
from django.http import JsonResponse
import re
import datetime
from dateutil import parser
class PassengerView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        if not request.user.is_driver and not request.user.is_organization:
            passengers = Passenger.objects.get(user=request.user)
            serializer = PassengerSerializer(passengers)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'error':'You are not a passenger'}, status=status.HTTP_400_BAD_REQUEST)
            
class PassengerChatbotView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.is_driver:
            question = request.data['question']
            res = DatabaseChatbot()
            output = res.generate_and_run_query(question)
            
            # Assuming `output` is a string that needs to be transformed
            # Transforming the string to a list of dictionaries
            return Response(output, status=status.HTTP_200_OK)
        if request.user.is_organization:
            question = request.data['question']
            res = DatabaseChatbot()
            output = res.generate_and_run_query(question)
            
            # Assuming `output` is a string that needs to be transformed
            # Transforming the string to a list of dictionaries
            return Response(output, status=status.HTTP_200_OK)
        else:
            question = request.data['question']
            res = DatabaseChatbot()
            output = res.generate_and_run_query(question)
            
            # Assuming `output` is a string that needs to be transformed
            # Transforming the string to a list of dictionaries
            return Response(output, status=status.HTTP_200_OK)
        


    