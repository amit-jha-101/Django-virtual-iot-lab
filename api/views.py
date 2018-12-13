from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .function import API
from rest_framework.decorators import api_view
from rest_framework import status
import json
from decimal import Decimal


# @api_view(['GET'])
# def clickapi(request, city="Mumbai"):
#     """
#     List all code snippets, or create a new snippet.
#     """
#     if request.method == 'GET':
#         api = API()
#         print(city)
#         data = api.getcity1JSON(city)

#         return Response(data)


@api_view(['POST'])
def postapi(request):
    if request.method == 'POST':
        api = API()
        data = request.body
        print(data)

        newData = json.loads(data)
        newData['Temperature'] = str(newData['Temperature'])
        flag = api.amazon(newData)
        if flag == True:
                return Response(status=status.HTTP_201_CREATED)
        else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
