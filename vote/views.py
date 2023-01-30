from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView


class LoginView(APIView):
    def get(self, request):
        code = request.data.get('code')
        print(code)
        return Response({'msg': 'nmsl'})

