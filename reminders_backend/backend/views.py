from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import ProfileSerializer


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