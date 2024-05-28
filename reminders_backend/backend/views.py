from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import ProfileSerializer
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
import json


# Create your views here.

@api_view(['GET'])
def get_routes(request):
    routes = [
        "/backend/token",
        '/backend/token/refresh'
    ]
    return Response(routes)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request):
    user = request.user
    profile = user.profile
    serializer = ProfileSerializer(profile, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_user(request):
    data = json.loads(request.body)
    for key,value in data.items():
        if value == "":
            return Response('Please fill all fields', status=status.HTTP_400_BAD_REQUEST)
    if data['password'] != data['passwordConfirmation']:
        return Response('Password do not match',status=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(username=data['username'])
        return Response('Username in use',status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        user = User.objects.create_user(username=data['username'],password=data['password'])
        return Response("User created",status=status.HTTP_200_OK)
