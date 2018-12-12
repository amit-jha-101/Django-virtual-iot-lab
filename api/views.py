from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .function import API
from rest_framework.decorators import api_view

@api_view(['GET'])
def clickapi(request,city="Mumbai"):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        api = API()
        print(city)
        data = api.getcity1JSON(city)
        
        return Response(data)