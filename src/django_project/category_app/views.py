from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK


class CategoryViewSet(viewsets.ViewSet):
    def list(self, request: Request):
        return Response(status=HTTP_200_OK, data=[
            {
                "id": "9bc466a6-b7ca-450c-9c59-033447112676",
                "name": "Movie",
                "description": "Movie description",
                "is_active": True
            },
            {
                "id": "6f7c2133-f1d3-4040-b700-c547453345d3",
                "name": "Documentary",
                "description": "Documentary description",
                "is_active": True
            }
        ])
