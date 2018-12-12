from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets, permissions
from .function import API
from rest_framework.decorators import api_view

# @api_view(['GET'])
# def clickapi(request,city="Mumbai"):
#     """
#     List all code snippets, or create a new snippet.
#     """
#     if request.method == 'GET':
#         api = API()
#         print(city)
#         data = api.getcity1JSON(city)
        
#         return Response(data)

class tempData(APIView):
    def get(self, request, city="Mumbai"):
        api = API()
        print(city)
        data = api.getcity1JSON(city)
        print(data)

        return Response(data)
