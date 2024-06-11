from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import ProfileSerializer
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
import json
from backend.models import *


# Create your views here.

@api_view(['GET'])
def get_routes(request):
    routes = [
        "/backend/token",
        '/backend/token/refresh'
    ]
    return Response(routes)

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def get_profile(request):
    if request.method == "GET":
        user = request.user
        try:
            profile = user.profile
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)
        except User.profile.RelatedObjectDoesNotExist:
            return Response({"user does not have a profile"}, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "POST":
        data = json.loads(request.body)
        #profile = Profile(user=request.user , first_name="jason",last_name="yes",email="foo@gmail.com")
        #profile.save()
        return Response({"profile created"}, status=status.HTTP_200_OK)

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
